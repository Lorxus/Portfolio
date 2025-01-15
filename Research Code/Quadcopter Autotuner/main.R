library(tidyverse)
data <- read.csv('LOG00047.01.CSV')
data$time..us. <- data$time..us./(1000*1000)
data$time..us. <- data$time..us. - data$time..us.[1]

data <- data %>% filter(time..us. > 24 & time..us. < 30)

signedSquare <- function(x) {
  return(sign(x) * x^2)
}

diff <- function(value, n) {
  return(
    value[-(1:n)] - value[1:(length(value) - n)]
  )
}

centralFiniteDiff <- function(value, time, n) {
  return(diff(value, n)/diff(time, n))
}

symmetricTruncate <- function(value, n) {
  return(value[(n/2):(length(value) - n/2 - 1)])
}

# Window size for first-order finite difference
window <- 10

timeSeconds <- data$time..us.
yawRateDegPerS <- data$gyroADC.2.
yawAccelDegPerSSquared <- centralFiniteDiff(yawRateDegPerS, timeSeconds, window)
pitchRateDegPerS <- data$gyroADC.1.
pitchAccelDegPerSSquared <- centralFiniteDiff(pitchRateDegPerS, timeSeconds, window)
rollRateDegPerS <- data$gyroADC.0.
rollAccelDegPerSSquared <- centralFiniteDiff(rollRateDegPerS, timeSeconds, window)
motorVelRPS <- data.frame(
  'frontLeft' = data$eRPM.0./6,
  'backLeft' = data$eRPM.1./6,
  'frontRight' = data$eRPM.2./6,
  'backRight' = data$eRPM.3./6)
motorAccelRPSSquared <- as.data.frame(
  lapply(motorVelRPS, function (vel) {
    return(centralFiniteDiff(vel, timeSeconds, window))
  })
)

# truncate non-differenced values to ensure signal alignment
timeSeconds <- symmetricTruncate(timeSeconds, window)
yawRateDegPerS <- symmetricTruncate(yawRateDegPerS, window)
rollRateDegPerS <- symmetricTruncate(rollRateDegPerS, window)
pitchRateDegPerS <- symmetricTruncate(pitchRateDegPerS, window)
motorVelRPS <- as.data.frame(
  lapply(motorVelRPS, function (vel) { return (symmetricTruncate(vel, window))})
)

yawDragLinear <- yawRateDegPerS
yawDragQuadratic <- signedSquare(yawDragLinear)
inertialAccel <- motorAccelRPSSquared$frontLeft - motorAccelRPSSquared$frontRight - motorAccelRPSSquared$backLeft + motorAccelRPSSquared$backRight  # signs depend on major (+) vs minor (-) diagonal
propDragLinear <- motorVelRPS$frontLeft - motorVelRPS$frontRight - motorVelRPS$backLeft + motorVelRPS$backRight
propDragQuadratic <- signedSquare(motorVelRPS$frontLeft) - signedSquare(motorVelRPS$frontRight) - signedSquare(motorVelRPS$backLeft) + signedSquare(motorVelRPS$backRight)
yawfit <- lm(yawAccelDegPerSSquared ~ yawDragLinear + yawDragQuadratic + inertialAccel + propDragLinear + propDragQuadratic)
summary(yawfit)

DISPLACEMENT_FRONT_MM <- 65
DISPLACEMENT_BACK_MM <- 88
DISPLACEMENT_LEFT_MM <- 1
DISPLACEMENT_RIGHT_MM <- 1

displacement_front_aspect <- 2.0 * DISPLACEMENT_FRONT_MM / (DISPLACEMENT_FRONT_MM + DISPLACEMENT_BACK_MM)
displacement_back_aspect <- 2.0 * DISPLACEMENT_BACK_MM / (DISPLACEMENT_FRONT_MM + DISPLACEMENT_BACK_MM)
displacement_left_aspect <- 2.0 * DISPLACEMENT_LEFT_MM / (DISPLACEMENT_LEFT_MM + DISPLACEMENT_RIGHT_MM)
displacement_right_aspect <- 2.0 * DISPLACEMENT_RIGHT_MM / (DISPLACEMENT_LEFT_MM + DISPLACEMENT_RIGHT_MM)

pitchDragLinear <- rollRateDegPerS
pitchDragQuadratic <- signedSquare(pitchDragLinear)
pitchThrustLinear <- displacement_front_aspect*(motorVelRPS$frontRight + motorVelRPS$frontLeft) - displacement_back_aspect*(motorVelRPS$backLeft + motorVelRPS$backRight)  # signs depend on front (+) vs back (-) side; we also need to account for front/back asymmetry
pitchThrustQuadratic <- displacement_front_aspect*(signedSquare(motorVelRPS$frontLeft) + signedSquare(motorVelRPS$frontRight)) - displacement_back_aspect*(signedSquare(motorVelRPS$backLeft) + signedSquare(motorVelRPS$backRight))  # 65 and 88 were found using parameter sweeps
pitchfit <- lm(pitchAccelDegPerSSquared ~ pitchDragLinear + pitchDragQuadratic + pitchThrustLinear + pitchThrustQuadratic)
summary(pitchfit)

rollDragLinear <- rollRateDegPerS
rollDragQuadratic <- signedSquare(rollDragLinear)
rollThrustLinear <- displacement_left_aspect*(motorVelRPS$frontLeft + motorVelRPS$backLeft) - displacement_right_aspect*(motorVelRPS$frontRight + motorVelRPS$backRight)  # signs depend on left (+) vs right (-) side; the quadcopter is bilaterally symmetric
rollThrustQuadratic <- displacement_left_aspect*(signedSquare(motorVelRPS$frontLeft) + signedSquare(motorVelRPS$backLeft)) - displacement_right_aspect(signedSquare(motorVelRPS$frontRight) + signedSquare(motorVelRPS$backRight))
rollfit <- lm(rollAccelDegPerSSquared ~ rollDragLinear + rollDragQuadratic + rollThrustLinear + rollThrustQuadratic)
summary(rollfit)

flatMotorVelRPS <- c(motorVelRPS$frontLeft, motorVelRPS$frontRight, motorVelRPS$backLeft, motorVelRPS$backRight)
flatMotorAccelRPSSquared <- c(motorAccelRPSSquared$frontLeft, motorAccelRPSSquared$frontRight, motorAccelRPSSquared$backLeft, motorAccelRPSSquared$backRight)

motorVelLinear <- flatMotorVelRPS
motorVelQuadratic <- signedSquare(motorVelLinear)
motorAccel <- flatMotorAccelRPSSquared
motorVoltage <- c(
  symmetricTruncate(data$motor.0./2047 * data$vbatLatest..V., window),
  symmetricTruncate(data$motor.1./2047 * data$vbatLatest..V., window),
  symmetricTruncate(data$motor.2./2047 * data$vbatLatest..V., window),
  symmetricTruncate(data$motor.3./2047 * data$vbatLatest..V., window)
)
voltfit <- lm(motorVoltage ~ 0 + motorVelLinear + motorVelQuadratic + motorAccel)
summary(voltfit)

# the full system equation in state-space form
# dX/dt = AX + BU
# because yaw depends on motor acceleration, not just velocity, len(X) is 11 - 4 motor velocities, 4 motor accelerations, and 3 rotational components

X_statevec <- list(yawRateDegPerS, pitchRateDegPerS, rollRateDegPerS, motorVelRPS$frontLeft, motorVelRPS$frontRight, motorVelRPS$backLeft, motorVelRPS$backRight, motorAccelRPSSquared$frontLeft, motorAccelRPSSquared$frontRight, motorAccelRPSSquared$backLeft, motorAccelRPSSquared$backRight)

# names = ['rho_yaw', 'rho_pitch', 'rho_roll', 'prop_drag_lin', 'prop_drag_quad', 'k_inertial', 'thrust_lin', 'thrust_quad', 'disp_front', 'disp_back', 'disp_left', 'disp_right', 'k_alpha', 'k_omega', 'k_omegasq']

coeffs_vec <- list(yawfit$coefficients$yawDragLinear, pitchfit$coefficients$pitchDragLinear, rollfit$coefficients$rollDragLinear,
                   yawfit$coefficients$propDragLinear, yawfit$coefficients$propDragQuadratic, yawfit$coefficients$inertialAccel,
                   pitchfit$coefficients$pitchThrustLinear, pitchfit$coefficients$pitchThrustQuadratic,
                   displacement_front_aspect, DISPLACEMENT_BACK_MM, DISPLACEMENT_LEFT_MM, DISPLACEMENT_RIGHT_MM,
                   voltfit$coefficients$motorAccel, voltfit$coefficients$motorVelLinear, voltfit$coefficients$motorVelQuadratic)

capture.output(coeffs_vec, file = 'regression_coefficients.csv')