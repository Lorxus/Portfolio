import math
import matplotlib.colors as mplcol
import matplotlib.patches as mplpat
import matplotlib.pyplot as mplplt
import numpy as np
import sklearn as skl
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd

SIGNARRAY = np.array([1, -1, -1, 1])  # varies by quadcopter. change back to 1 -1 1 -1 for the earlier csvs.
STARTSEC = 6
ENDSEC = 11

# each successive row represents 0.5ms
YAW_INCREMENT = 50
VOLT_INCREMENT = 10

# load data
filename = 'LOG00043.01.csv'
qc_raw = open(filename, 'r')
qc_log = qc_raw.read()
qc_raw.close()

# clean data - initial
qc_data = qc_log.split('\n')
qc_data = qc_data[1:-1]  # trim headers and last blank row

# clean data - main
timestamp = []  # time
motorVel_RPS = []  # eRPM0--3; FL, FR, BR, BL
yawVel_DPS = []  # gyroADC2 is yaw

# easier than figuring out how to tell pandas that the separator is ',  '...
qc_df = pd.read_csv(filename)

timestamp = qc_df[' time (us)']                                                 # timestamps in microseconds
motorVel_RPS = qc_df[[' eRPM[0]', ' eRPM[1]', ' eRPM[2]', ' eRPM[3]']]          # motor rotations in RPM
yawVel_DPS = qc_df[' gyroADC[2]']                                               # dYaw/dt measurements
vbat = qc_df[' vbatLatest (V)']                                                 # battery voltage
motorVoltages = qc_df[[' motor[0]', ' motor[1]', ' motor[2]', ' motor[3]']]     # motor voltages

timestamp = np.array(timestamp)/1000000.  # convert from microseconds to seconds; align to have the start time be 0
timestamp -= (min(timestamp) - 0.0000001)
motorVel_RPS = np.array(motorVel_RPS)
yawVel_DPS = np.array(yawVel_DPS)
vbat = np.array(vbat)
motorVoltages = np.array(motorVoltages) * (vbat[:, np.newaxis]) * (1.0 / 2047.)  # convert from 12-bit voltage readings to actual absolute voltages

fakedt = float(timestamp[1]-timestamp[0])  # this is not the way I would clip out a section of telemetry if I wanted to do it right...
startidx = int(STARTSEC/fakedt)
endidx = int(ENDSEC/fakedt)

timestamp = timestamp[startidx:endidx]
motorVel_RPS = motorVel_RPS[startidx:endidx] * (1.0 / 6.)  # unsigned version; convert from RPdM to RPS
yawVel_DPS = yawVel_DPS[startidx:endidx]
motorVoltages = motorVoltages[startidx:endidx]

motorVel_SgnRPS = np.copy(motorVel_RPS)  # this will hold the signed motor RPS values, bundled together
motorVel_SgnRPS = motorVel_SgnRPS * SIGNARRAY  # needed sign alterations
motor_SgnRPSTotal = np.sum(motorVel_SgnRPS, axis=1)  # this will hold the rowwise (axis 1) sum of the signed motor RPS values

# discrete differentials - yaw
print('yaw section')
yaw_dt = timestamp[YAW_INCREMENT:] - timestamp[:-YAW_INCREMENT]
motorsAcc_RPSqS = (motorVel_SgnRPS[YAW_INCREMENT:] - motorVel_SgnRPS[:-YAW_INCREMENT]) / (np.column_stack((yaw_dt, yaw_dt, yaw_dt, yaw_dt)))
yawAcc_DPSqS = (yawVel_DPS[YAW_INCREMENT:] - yawVel_DPS[:-YAW_INCREMENT]) / yaw_dt
motorAcc_SgnRPSTotal = np.sum(motorsAcc_RPSqS, axis=1)

# YAW REGRESSION
# gamma_dot_dot = kDrag * gamma_dot + sum_motor (kInertia * omega_dot + tauLin * omega + tauQuad * omega^2)
# so we need to fit x_1 = gamma_dot, x_2 = omega_dot, x_3 = omega, x_4 = omega^2 against y = gamma_dot_dot
# and get k_1 = kDrag, k_2 = kInertia, k_3 tauLin, k_4 = tauQuad

motorsVelSq = motorVel_SgnRPS * motorVel_SgnRPS * np.sign(motorVel_SgnRPS)
motorSqVel_SqRPS = np.sum(motorsVelSq, axis=1)

# according to a test in R, neither omega nor gamma_dot have strongly significant correlation with gamma_dot_dot
yawData_X = {'omega_dot': list(motorAcc_SgnRPSTotal),  # coeff is kInertia
             'omega_sq': list(motorSqVel_SqRPS)[YAW_INCREMENT // 2:-YAW_INCREMENT // 2],  # coeff is tauQuad
             'omega': list(motor_SgnRPSTotal)[YAW_INCREMENT // 2:-YAW_INCREMENT // 2],  # coeff is tauLin
             'gamma_dot': list(yawVel_DPS)[YAW_INCREMENT // 2:-YAW_INCREMENT // 2]}  # coeff is kDrag
yaw_df_X = pd.DataFrame(data=yawData_X)

yawData_Y = {'gamma_dot_dot': list(yawAcc_DPSqS)}
yaw_df_Y = pd.DataFrame(data=yawData_Y)

yaw_model = LinearRegression()
yaw_model.fit(yaw_df_X.values, yaw_df_Y.values)
print('Yaw Coefficients:', yaw_model.coef_)
print('Yaw Intercept:', yaw_model.intercept_)

# projection plots: an independent variable from datapts_X against the regression-predicted linear combination of datapts_Y and the rest of datapts_X  
plot_X_yawDeriv = np.array(yaw_df_X['omega_dot'].values)
plot_Y_yawDeriv = yaw_model.intercept_[0] + np.array(yaw_df_Y.values).T - (np.array(yaw_df_X['omega_sq'].values) * yaw_model.coef_[0][1]) - (np.array(yaw_df_X['omega'].values) * yaw_model.coef_[0][2]) - (np.array(yaw_df_X['gamma_dot'].values) * yaw_model.coef_[0][3])
yawDeriv_predY = np.polynomial.polynomial.polyval(plot_X_yawDeriv, [yaw_model.intercept_[0], yaw_model.coef_[0][0]])

plot_X_rotSq = np.array(yaw_df_X['omega_sq'].values)
plot_Y_rotSq = yaw_model.intercept_[0] + np.array(yaw_df_Y.values).T - (np.array(yaw_df_X['omega_dot'].values) * yaw_model.coef_[0][0]) - (np.array(yaw_df_X['omega'].values) * yaw_model.coef_[0][2]) - (np.array(yaw_df_X['gamma_dot'].values) * yaw_model.coef_[0][3])
rotSq_predY = np.polynomial.polynomial.polyval(plot_X_rotSq, [yaw_model.intercept_[0], yaw_model.coef_[0][1]])

# plot of inertial acceleration fit against predicted combination of other vars
mplplt.scatter(plot_X_yawDeriv, plot_Y_yawDeriv, color='black', marker='.')
mplplt.plot(plot_X_yawDeriv, yawDeriv_predY, color = 'red')
mplplt.title('Inertial Acceleration vs (dYaw/dt & Other Independents)')
mplplt.xlabel('Inertial Acceleration')
mplplt.ylabel('dYaw/dt + Fit Intercept - Sum(Fit Coefficients * [Linear Prop Drag, Squared Prop Drag, Inertial Drag])')
mplplt.show()

# plot of squared drag term fit against predicted combination of other vars
mplplt.scatter(plot_X_rotSq, plot_Y_rotSq, color='black', marker='.')
mplplt.plot(plot_X_rotSq, rotSq_predY, color = 'blue')
mplplt.title('Squared Prop Drag vs (dYaw/dt & Other Independents)')
mplplt.xlabel('Squared Prop Drag')
mplplt.ylabel('dYaw/dt + Fit Intercept - Sum(Fit Coefficients * [Linear Prop Drag, Inertial Drag, Inertial Acceleration])')
mplplt.show()

print('volt section')
# discrete differentials - voltage
volt_dt = timestamp[VOLT_INCREMENT:] - timestamp[:-VOLT_INCREMENT]

allmotorVel_RPS = motorVel_RPS[VOLT_INCREMENT // 2:-VOLT_INCREMENT // 2].flatten(order='F')  # this will hold the unsigned motor RPS values, concatenated columnwise
motorAcc_RPSqS = (motorVel_RPS[VOLT_INCREMENT:] - motorVel_RPS[:-VOLT_INCREMENT]) / (np.column_stack((volt_dt, volt_dt, volt_dt, volt_dt)))  # something is wrong with how I calculate this...
allmotorAcc_RPSqS = motorAcc_RPSqS.flatten(order='F')
allmotorVoltages = motorVoltages[VOLT_INCREMENT // 2:-VOLT_INCREMENT // 2].flatten(order='F')  # this will hold the voltage readings, concatenated in the same way

# VOLTAGE REGRESSION
# V = sum_motor(omega/k_omega + omega_sq/k_quad + omega_dot/k_dot); we don't need to worry about sign alterations here because the dynamics are all motor-internal

allmotorSqVel_SqRPS = allmotorVel_RPS * allmotorVel_RPS

voltdatapts_X = {'omega': list(allmotorVel_RPS),  # coeff is 1/k_dot
                'omega_sq': list(allmotorSqVel_SqRPS),  # coeff is 1/k_quad
                'omega_dot': list(allmotorAcc_RPSqS)}  # coeff is 1/k_omega

vdf_X = pd.DataFrame(data=voltdatapts_X)

voltdatapts_Y = {'concat_volts': list(allmotorVoltages)}
vdf_Y = pd.DataFrame(data=voltdatapts_Y)

volt_model = LinearRegression(fit_intercept=False)  # at 0 volts, there should be no motion
volt_model.fit(vdf_X.values, vdf_Y.values)
print('Voltage Coefficients:', volt_model.coef_)
print('Voltage Intercept:', volt_model.intercept_)

volt_pred = np.array(vdf_X['omega'].values * volt_model.coef_[0][0]) + np.array(vdf_X['omega_sq'].values * volt_model.coef_[0][1]) + np.array(vdf_X['omega_dot'].values * volt_model.coef_[0][2])  # coeff_ == 0
print(skl.metrics.r2_score(np.array(vdf_Y['concat_volts'].values), volt_pred))

# plot of motor speed fit against predicted combination of other vars
plot_X_rot = np.array(vdf_X['omega'].values)
plot_Y_rot = np.array(vdf_Y.values).T - (np.array(vdf_X['omega_sq'].values) * volt_model.coef_[0][1]) - (np.array(vdf_X['omega_dot'].values) * volt_model.coef_[0][2])
rot_predY = np.polynomial.polynomial.polyval(plot_X_rot, [0, volt_model.coef_[0][0]])

mplplt.scatter(plot_X_rot, plot_Y_rot, color='black', marker='.')
mplplt.plot(plot_X_rot, rot_predY, color ='green')
mplplt.title('Motor Rotational Speed vs (Voltage & Other Independents)')
mplplt.xlabel('Motor RPS')
mplplt.ylabel('Voltage - Sum(Fit Coefficients * [Squared Prop Drag, Prop Acceleration])')
mplplt.show()

# plot of motor acceelration fit against predicted combination of other vars
plot_X_rot = np.array(vdf_X['omega_dot'].values)
plot_Y_rot = np.array(vdf_Y.values).T - (np.array(vdf_X['omega'].values) * volt_model.coef_[0][0]) - (np.array(vdf_X['omega_sq'].values) * volt_model.coef_[0][1])
acc_predY = np.polynomial.polynomial.polyval(plot_X_rot, [0, volt_model.coef_[0][2]])

mplplt.scatter(plot_X_rot, plot_Y_rot, color='black', marker='.')
mplplt.plot(plot_X_rot, acc_predY, color ='orange')
mplplt.title('Motor Acceleration vs (Voltage & Other Independents)')
mplplt.xlabel('Motor Acceleration RPS^2')
mplplt.ylabel('Voltage - Sum(Fit Coefficients * [Prop Drag, Squared Prop Drag])')
mplplt.show()

print('done')