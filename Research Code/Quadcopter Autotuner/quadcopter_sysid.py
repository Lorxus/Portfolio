import numpy as np
import control as ct
import json

def k_beta(d: dict, curr_motor: float) -> float:
	alpha = d['k_alpha']
	omega = d['k_omega']
	omegasq = d['k_omegasq']
	res = alpha * ((1.0/omega) + (2.0*curr_motor/omegasq))
	return res

def makerow_A_yaw(d: dict, motors: list[float]) -> list[float]:
	res = [0] * 7
	res[0] = d['rho_yaw']
	res[3] = d['prop_drag_lin'] + 2 * motors[0] * d['prop_drag_quad'] + d['k_inertial'] * k_beta(d, motors[0])
	res[4] = -1 * d['prop_drag_lin'] + 2 * motors[1] * d['prop_drag_quad'] - d['k_inertial'] * k_beta(d, motors[1])
	res[5] = -1 * d['disp_back'](d['prop_drag_lin'] + 2 * motors[2] * d['prop_drag_quad']) - d['k_inertial'] * k_beta(d, motors[2])
	res[6] = d['prop_drag_lin'] + 2 * motors[3] * d['prop_drag_quad'] + d['k_inertial'] * k_beta(d, motors[3])
	return np.array(res)

def makerow_A_pitch(d: dict, motors: list[float]) -> list[float]:
	res = [0] * 7
	res[1] = d['rho_pitch']
	res[3] = d['disp_front'](d['thrust_lin'] + 2 * motors[0] * d['thrust_quad'])
	res[4] = d['disp_front'](d['thrust_lin'] + 2 * motors[1] * d['thrust_quad'])
	res[5] = -1 * d['disp_back'](d['thrust_lin'] + 2 * motors[2] * d['thrust_quad'])
	res[6] = -1 * d['disp_back'](d['thrust_lin'] + 2 * motors[3] * d['thrust_quad'])
	return np.array(res)

def makerow_A_roll(d: dict, motors: list[float]) -> list[float]:
	res = [0] * 7
	res[2] = d['rho_roll']
	res[3] = d['disp_left'](d['thrust_lin'] + 2 * motors[0] * d['thrust_quad'])
	res[4] = -1 * d['disp_right'](d['thrust_lin'] + 2 * motors[1] * d['thrust_quad'])
	res[5] = d['disp_left'](d['thrust_lin'] + 2 * motors[2] * d['thrust_quad'])
	res[6] = -1 * d['disp_right'](d['thrust_lin'] + 2 * motors[3] * d['thrust_quad'])
	return np.array(res)

def makerow_A_omega(d: dict, motors: list[float], idx: int) -> list[float]:
	# idx controls which motor
	# 0 = FL, 1 = FR, 2 = BL, 3 = BR
	res = [0] * 7
	res[3 + idx] = k_beta(d, motors[idx])
	return np.array(res)


if __name__ == '__main__':
	# read in file of coefficients
	filename = 'regression_coefficients.json'
	qc_raw = open(filename, 'r')
	qc_log = json.load(qc_raw)
	qc_raw.close()

	motors = [float, float, float, float]

	# make dict of params
	qc_params = json.loads(qc_log)
	# qc_params = {}
	# names = ['rho_yaw', 'rho_pitch', 'rho_roll', 'prop_drag_lin', 'prop_drag_quad', 'k_inertial', 'thrust_lin', 'thrust_quad', 'disp_front', 'disp_back', 'disp_left', 'disp_right', 'k_alpha', 'k_omega', 'k_omegasq']
	# for idx, n_ in enumerate(names):
	# 	qc_params[n_] = float(qc_log[idx])

	# run each 'makerow' function and compile the rows into matrix A (linear dynamics)
	qc_state_matrix_A = np.array([makerow_A_yaw(qc_params, motors), makerow_A_pitch(qc_params, motors),
	                     makerow_A_roll(qc_params, motors)])
	for i in range(4):
		qc_state_matrix_A.np.append(makerow_A_omega(qc_params, motors, i))

	# directly assemble matrix B (voltage-based control)
	inertialalpha = qc_params['k_alpha'] * qc_params['k_inertial']
	qc_state_matrix_B = np.array([[inertialalpha, -inertialalpha, -inertialalpha, inertialalpha], [0] * 4, [0] * 4,
	                     [qc_params['k_alpha'], 0, 0, 0], [0, qc_params['k_alpha'], 0, 0],
	                     [0, 0, qc_params['k_alpha'], 0], [0, 0, 0, qc_params['k_alpha']]])

	# directly assemble matrix C (affine term)
	qc_state_matrix_C = np.array([qc_params['prop_drag_quad'] + (qc_params['k_alpha'] * qc_params['k_inertial'])/qc_params['k_omega**2'] * (- motors[0]**2 + motors[1]**2 + motors[2]**2 - motors[3]**2),
	                              qc_params['thrust_quad'] * (qc_params['disp_back'] * (motors[2]**2 + motors[3]**2 ) - qc_params['disp_front'] * (motors[0]**2 + motors[1]**2)),
	                              qc_params['thrust_quad'] * (qc_params['disp_right'] * (motors[1]**2 + motors[3]**2 ) - qc_params['disp_left'] * (motors[0]**2 + motors[2]**2)),
	                              qc_params['k_alpha'] * motors[0]**2 / qc_params['k_omegasq'],
	                              qc_params['k_alpha'] * motors[1]**2 / qc_params['k_omegasq'],
	                              qc_params['k_alpha'] * motors[2]**2 / qc_params['k_omegasq'],
	                              qc_params['k_alpha'] * motors[3]**2 / qc_params['k_omegasq']])