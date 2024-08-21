# tests RAFT FOWT functionality and results

import pytest
import numpy as np
from numpy.testing import assert_allclose
import yaml
import pickle
import raft
import os

'''
 Define files for testing
'''
# Name of the subfolder where the test data is located
test_dir = 'test_data'

# List of input file names to be tested
list_files = [
    'VolturnUS-S.yaml',
    'OC3spar.yaml',
]


# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# To avoid problems with different platforms, get the full path of the file
list_files = [os.path.join(current_dir, test_dir, file) for file in list_files]


'''
 Desired values to compare with the results.
 Should be lists of the same length as list_files.
 List elements are indicated below.
'''
# Structure related quantities
desired_rCG = [
    np.array([ 2.34101810e-15,  7.81354773e-16,   -1.96876014e+00]),
    np.array([              0,               0,  -78.01639837    ]),
]
desired_rCG_sub = [
    np.array([ 2.65203563e-15,  8.85162184e-16,  -1.51939447e+01]),
    np.array([              0,               0, -89.91292526    ]),
]

desired_m_ballast = [
    np.array([1.0569497625e+07, 2.42678207158787e+06]),
    np.array([6.5323524956e+06])
]

desired_M_struc = [
    np.array([[  1.91081767e+07,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -3.76194166e+07, -1.49302650e-08],
              [  0.00000000e+00,  1.91081767e+07,  0.00000000e+00,  3.76194166e+07,  0.00000000e+00,  4.47325874e-08],
              [  0.00000000e+00,  0.00000000e+00,  1.91081767e+07,  1.49302650e-08, -4.47325874e-08,  0.00000000e+00],
              [  0.00000000e+00,  3.76194166e+07,  1.49302650e-08,  4.25734293e+10,  9.54605630e-07,  4.76371497e-07],
              [ -3.76194166e+07,  0.00000000e+00, -4.47325874e-08,  9.54605639e-07,  4.25734293e+10,  4.76371497e-07],
              [ -1.49302650e-08,  4.47325874e-08,  0.00000000e+00,  5.96046448e-07,  4.76371497e-07,  2.05595816e+10]]),
    np.array([[  8.08951257e+06,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -6.31114635e+08,  0.00000000e+00],
              [  0.00000000e+00,  8.08951257e+06,  0.00000000e+00,  6.31114635e+08,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  8.08951257e+06,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  6.31114635e+08,  0.00000000e+00,  6.77668985e+10,  0.00000000e+00,  0.00000000e+00],
              [ -6.31114635e+08,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.77576144e+10,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.18030295e+08]]),
]

desired_M_struc_sub = [
    np.array([[  1.68672649e+07,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -2.56280290e+08, -1.49302650e-08],
              [  0.00000000e+00,  1.68672649e+07,  0.00000000e+00,  2.56280290e+08,  0.00000000e+00,  4.47325874e-08],
              [  0.00000000e+00,  0.00000000e+00,  1.68672649e+07,  1.49302650e-08, -4.47325874e-08,  0.00000000e+00],
              [  0.00000000e+00,  2.56280290e+08,  1.49302650e-08,  1.49458996e+10,  9.54605639e-07,  4.76371497e-07],
              [ -2.56280290e+08,  0.00000000e+00, -4.47325874e-08,  9.54605639e-07,  1.49458996e+10,  4.76371497e-07],
              [ -1.49302650e-08,  4.47325874e-08,  0.00000000e+00,  5.96046448e-07,  4.76371497e-07,  2.05313182e+10]]),
    np.array([[  7.48986700e+06,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -6.73435852e+08,  0.00000000e+00],
              [  0.00000000e+00,  7.48986700e+06,  0.00000000e+00,  6.73435852e+08,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  7.48986700e+06,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  6.73435852e+08,  0.00000000e+00,  6.43071810e+10,  0.00000000e+00,  0.00000000e+00],
              [ -6.73435852e+08,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.43071810e+10,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  9.00523426e+07]])
]

desired_C_struc = [
    np.array([[  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  3.69046477e+08,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  3.69046477e+08,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]]),
    np.array([[  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00], 
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00], 
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.19123457e+09,  0.00000000e+00,  0.00000000e+00], 
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  6.19123457e+09,  0.00000000e+00], 
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]]),
]

desired_W_struc = [
    np.array([  0.00000000e+00,  0.00000000e+00, -1.87451213e+08, -2.38651410e-07,  3.58093530e-07,  0.00000000e+00]),
    np.array([  0.00000000e+00,  0.00000000e+00, -7.93581183e+07,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]),
]

# Hydrostatic quantities
desired_rCB = [
    np.array([ 3.04454348e-15,  1.52227174e-15, -1.35855138e+01]),
    np.array([ 0.00000000e+00,  0.00000000e+00, -6.20656552e+01]),
]

desired_C_hydro = [
    np.array([[  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  4.30992285e+06, -7.45058060e-09,  2.23517418e-08,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00, -7.45058060e-09,  2.17117691e+09, -4.76837158e-07,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  2.23517418e-08, -4.76837158e-07,  2.17117691e+09,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]]),
    np.array([[  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  3.33664089e+05,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -5.01003340e+09,  0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -5.01003340e+09,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]]),
]

desired_W_hydro = [
    np.array([ 0.00000000e+00,  0.00000000e+00,  1.92243134e+08,  2.38418579e-07, -3.57627869e-07,  0.00000000e+00]),
    np.array([ 0.00000000e+00,  0.00000000e+00,  8.07357058e+07,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00])
]


# Hydrodynamic quantities
desired_A_hydro_morison = [
    np.array([[  1.23332103e+07,  4.65661287e-10,  0.00000000e+00,  7.45058060e-09, -1.54950929e+08, -2.98023224e-08],
              [  4.65661287e-10,  1.23332103e+07, -2.58493941e-26,  1.54950929e+08, -7.45058060e-09,  7.45058060e-08],
              [  0.00000000e+00, -2.58493941e-26,  1.09392236e+07,  1.49011612e-08, -1.49011612e-08, -9.18354962e-41],
              [  7.45058060e-09,  1.54950929e+08,  1.49011612e-08,  7.44302567e+09,  3.57627869e-07,  9.53674316e-07],
              [ -1.54950929e+08, -7.45058060e-09, -1.49011612e-08,  3.57627869e-07,  7.44302567e+09,  4.76837158e-07],
              [ -2.98023224e-08,  7.45058060e-08, -9.18354962e-41,  8.34465027e-07,  4.76837158e-07,  2.39620560e+10]]),
    np.array([[  8.22881104e+06,  0.00000000e+00,  0.00000000e+00, 0.00000000e+00,  -5.10692712e+08,  0.00000000e+00],
              [  0.00000000e+00,  8.22881104e+06,  0.00000000e+00, 5.10692712e+08,   0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  2.23242607e+05, 0.00000000e+00,   0.00000000e+00,  0.00000000e+00],
              [  0.00000000e+00,  5.10692712e+08,  0.00000000e+00, 4.09467123e+10,   0.00000000e+00,  0.00000000e+00],
              [ -5.10692712e+08,  0.00000000e+00,  0.00000000e+00, 0.00000000e+00,   4.09467123e+10,  0.00000000e+00],
              [  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, 0.00000000e+00,   0.00000000e+00,  0.00000000e+00]])
]

desired_F_hydro_iner = [
    np.array([[[  0.00000000e+00+0.00000000e+00j,  5.27862388e-06+3.55202739e-04j,  2.70437607e+03+7.13012568e+04j,  1.39204693e+05+1.20341600e+06j,  6.19003712e+05+1.45322648e+06j,  1.26581615e+06+5.38094639e+05j,  1.54066254e+06-1.06700055e+05j,  9.73449433e+05-1.54735127e+05j, -7.25098731e+04-1.53049868e+05j, -5.50225753e+05-2.51854400e+05j],
               [  0.00000000e+00+0.00000000e+00j,  0.00000000e+00-6.77626358e-21j,  0.00000000e+00-9.09494702e-13j,  2.91038305e-11+0.00000000e+00j, -2.91038305e-11-1.45519152e-11j, -5.09317033e-11+2.91038305e-11j,  0.00000000e+00-2.18278728e-11j,  7.27595761e-12-1.81898940e-11j, -3.63797881e-12-9.09494702e-13j,  0.00000000e+00+1.36424205e-12j],
               [  0.00000000e+00+0.00000000e+00j,  4.36781698e-04-1.06335971e-06j,  1.12590567e+04-7.39559352e+02j, -3.67100235e+05-3.03329514e+04j, -9.33433420e+05-5.29491702e+04j, -7.56882469e+05+4.71609883e+04j, -3.08614019e+05+2.21762147e+05j, -3.10898556e+04+3.10700182e+05j,  4.30529645e+04+2.41235701e+05j,  4.57382992e+04+1.05934499e+05j],
               [  0.00000000e+00+0.00000000e+00j,  1.95156391e-18+4.87890978e-19j,  8.73114914e-11+4.36557457e-11j,  9.31322575e-10+9.31322575e-10j, -9.31322575e-10+1.86264515e-09j, -1.39698386e-09-9.31322575e-10j, -2.03726813e-10-8.14907253e-10j,  5.82076609e-10+0.00000000e+00j,  3.20142135e-10-1.09139364e-10j,  1.45519152e-11+5.09317033e-11j],
               [  0.00000000e+00+0.00000000e+00j, -5.25125306e-04-1.13258648e-04j, -1.88802798e+05-2.34251669e+05j, -5.03535064e+06-9.34753238e+06j, -9.66951530e+06-2.29999628e+07j, -9.07389415e+06-2.31167534e+07j, -7.24707025e+06-1.36646621e+07j, -4.98264131e+06-4.74474286e+06j, -1.64674075e+06-6.23579171e+04j,  4.05694750e+05+1.24236863e+06j],
               [  0.00000000e+00+0.00000000e+00j,  1.49077799e-19-2.71050543e-19j, -1.81898940e-11+7.27595761e-12j,  1.51339918e-09-6.98491931e-10j,  0.00000000e+00+1.16415322e-09j, -1.62981451e-09+1.97906047e-09j,  3.02679837e-09-1.48429535e-09j, -7.56699592e-10+5.23868948e-10j,  1.13504939e-09+9.24046617e-10j, -4.36557457e-11-9.31322575e-10j]]]),
    np.array([[[  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+1.29014243e-04j,  0.00000000e+00+2.18136450e+04j,  0.00000000e+00+3.20625334e+05j,  0.00000000e+00+4.47063970e+05j,  0.00000000e+00+3.72186312e+05j,  0.00000000e+00+2.73435771e+05j,  0.00000000e+00+1.96646986e+05j,  0.00000000e+00+1.42846361e+05j,  0.00000000e+00+1.05877244e+05j],
               [  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j],
               [  0.00000000e+00+0.00000000e+00j, -3.83018423e-06+0.00000000e+00j, -4.39079984e+03+0.00000000e+00j, -7.61182325e+04+0.00000000e+00j, -1.07109629e+05+0.00000000e+00j, -8.59303021e+04+0.00000000e+00j, -5.94885784e+04+0.00000000e+00j, -3.95278075e+04+0.00000000e+00j, -2.59659374e+04+0.00000000e+00j, -1.70032358e+04+0.00000000e+00j],
               [  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j],
               [  0.00000000e+00+0.00000000e+00j,  0.00000000e+00-7.11328048e-03j,  0.00000000e+00-1.01290133e+06j,  0.00000000e+00-1.16863323e+07j,  0.00000000e+00-1.21895057e+07j,  0.00000000e+00-7.55633166e+06j,  0.00000000e+00-4.23360829e+06j,  0.00000000e+00-2.38627057e+06j,  0.00000000e+00-1.38694212e+06j,  0.00000000e+00-8.34570909e+05j],
               [  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j]]])
]


desired_B_hydro_drag = [
    np.array([[ 5.45662701e+05, -7.15119914e+03,  6.17751247e-13, -1.17994786e+05, -6.51642363e+06, -2.35546868e+05],
              [-7.15119914e+03,  4.99246284e+05,  8.45248506e-13,  5.75055274e+06,  1.17994786e+05,  1.17740407e+06],
              [ 6.17751247e-13,  8.45248506e-13,  6.20306804e+05, -6.33559493e+05,  1.05919467e+06, -1.74451334e-26],
              [-1.17994786e+05,  5.75055274e+06, -6.33559493e+05,  4.06876060e+08,  1.45945247e+07,  1.99459587e+07],
              [-6.51642363e+06,  1.17994786e+05,  1.05919467e+06,  1.45945247e+07,  4.69086461e+08,  3.77038199e+06],
              [-2.35546868e+05,  1.17740407e+06, -1.74451334e-26,  1.99459587e+07,  3.77038199e+06,  9.94441241e+08]]),
    np.array([[ 2.74533181e+05,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00, -1.60581567e+07,  0.00000000e+00],
              [ 0.00000000e+00,  2.74533181e+05,  0.00000000e+00,  1.60581567e+07,  0.00000000e+00,  0.00000000e+00],
              [ 0.00000000e+00,  0.00000000e+00,  1.42596928e+04,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
              [ 0.00000000e+00,  1.60581567e+07,  0.00000000e+00,  1.33888631e+09,  0.00000000e+00,  0.00000000e+00],
              [-1.60581567e+07,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.33888631e+09,  0.00000000e+00],
              [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00]])
]


desired_F_hydro_drag = [
    np.array([[ 6.26798938e+04-1.06576584e+03j,  7.00748475e+04-2.89201688e+03j,  8.12157593e+04-7.38829784e+03j,  7.99202139e+04-1.71186649e+04j,  5.70971129e+04-3.47002772e+04j,  2.27393403e+04-5.91662066e+04j, -9.11605006e+02-7.46368022e+04j, -3.93986729e+03-5.28862578e+04j, -6.65220062e+03+5.67359238e+03j, -1.69638473e+04+4.21813590e+04j],
              [-8.17879804e+02+2.01664178e+01j, -9.05916942e+02+5.37256226e+01j, -1.06142727e+03+1.27811882e+02j, -1.14594284e+03+2.46346476e+02j, -1.08284917e+03+3.71666065e+02j, -8.99454707e+02+4.63199882e+02j, -6.52221403e+02+4.91741004e+02j, -4.03273261e+02+4.50941473e+02j, -2.01267908e+02+3.58647869e+02j, -6.89581470e+01+2.46686181e+02j],
              [-1.77809837e+02+3.53096509e+04j, -7.69294843e+02+6.69317300e+04j, -1.59218418e+03+8.56500799e+04j, -6.35173799e+02+8.25191935e+04j,  5.57887851e+03+5.97731749e+04j,  1.74915780e+04+2.91254328e+04j,  2.82101053e+04+5.97781075e+03j,  2.82523466e+04-3.37727649e+03j,  1.75318029e+04-4.87317440e+03j,  6.14168092e+03-4.91705071e+03j],
              [-1.56472514e+04-3.56587820e+04j, -2.48269966e+04-6.75219656e+04j, -4.38895803e+04-8.63885154e+04j, -6.81958252e+04-8.39637038e+04j, -8.69317275e+04-6.16864051e+04j, -9.07206914e+04-2.72968838e+04j, -7.61908158e+04+6.34413732e+03j, -4.90030653e+04+2.71940946e+04j, -2.08007832e+04+3.08174173e+04j, -1.68683359e+03+2.21114763e+04j],
              [-8.09154770e+05+7.55521730e+04j, -1.11405014e+06+1.38036829e+05j, -1.69807564e+06+1.40122712e+05j, -2.24660955e+06+6.88066942e+03j, -2.29164518e+06-1.96910910e+05j, -1.68275633e+06-2.16158480e+05j, -8.02830099e+05+8.95925792e+04j, -2.21953451e+05+4.07670931e+05j, -2.34817229e+04+3.35670454e+05j,  5.97818333e+04+6.55288898e+04j],
              [-2.69557437e+04+8.22032373e+02j, -2.99071017e+04+2.20326250e+03j, -3.50857908e+04+5.29644988e+03j, -3.77525771e+04+1.03521333e+04j, -3.50996064e+04+1.58615801e+04j, -2.77949860e+04+1.99887416e+04j, -1.77777631e+04+2.10771386e+04j, -7.75396152e+03+1.83252193e+04j, -5.20602493e+02+1.24185446e+04j,  2.16541766e+03+5.69240330e+03j]]),
    np.array([[ 2.42524989e+04+0.00000000e+00j,  2.53551307e+04+0.00000000e+00j,  2.58043349e+04+0.00000000e+00j,  2.38396747e+04+0.00000000e+00j,  2.16381681e+04+0.00000000e+00j,  1.99920899e+04+0.00000000e+00j,  1.87681469e+04+0.00000000e+00j,  1.77647183e+04+0.00000000e+00j,  1.68784735e+04+0.00000000e+00j,  1.60659931e+04+0.00000000e+00j], 
              [ 0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j],
              [ 0.00000000e+00+7.39494781e+02j,  0.00000000e+00+1.34129117e+03j,  0.00000000e+00+1.66090919e+03j,  0.00000000e+00+1.87063995e+03j,  0.00000000e+00+2.03604503e+03j,  0.00000000e+00+2.12322733e+03j,  0.00000000e+00+2.11451413e+03j,  0.00000000e+00+2.01913306e+03j,  0.00000000e+00+1.85790505e+03j,  0.00000000e+00+1.65411694e+03j],
              [ 0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j],
              [-1.36949214e+06+0.00000000e+00j, -1.25578704e+06+0.00000000e+00j, -9.97042126e+05+0.00000000e+00j, -6.46386615e+05+0.00000000e+00j, -3.89000599e+05+0.00000000e+00j, -2.44659044e+05+0.00000000e+00j, -1.67285667e+05+0.00000000e+00j, -1.22492723e+05+0.00000000e+00j, -9.38820976e+04+0.00000000e+00j, -7.42323180e+04+0.00000000e+00j],
              [ 0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j,  0.00000000e+00+0.00000000e+00j]])
]


desired_current_drag = [
    np.array([2.64655964e+06, 6.47726496e+05, 7.60648090e-27, 8.77357984e+06, -3.65254345e+07, 1.15751779e+07]),
    np.array([1.66747692e+06, 4.46799093e+05,        0.0e+00, 2.67342887e+07, -9.97737237e+07,        0.0e+00])
]

'''
 Aux functions
'''
# Function used to create FOWT instance
# Not explicitly inside the fixture below so that we can also run this file as a script
# 
def create_fowt(file):
    with open(file) as f:
        design = yaml.load(f, Loader=yaml.FullLoader)        
    fowt = raft.Model(design).fowtList[0]
    fowt.setPosition(np.zeros(6))
    fowt.calcStatics()
    return fowt

# Define a fixture to loop fowt instances with the index to loop the desired values as well
# Could also zip the lists with the desired values, but I think the approach below is simpler
@pytest.fixture(params=enumerate(list_files))
def index_and_fowt(request):
    index, file = request.param
    fowt = create_fowt(file)    
    return index, fowt


'''
 Test functions
'''
def test_statics(index_and_fowt):
    index, fowt = index_and_fowt    

    # Structure related quantities
    assert_allclose(fowt.rCG, desired_rCG[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.rCG_sub, desired_rCG_sub[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.m_ballast, desired_m_ballast[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.M_struc, desired_M_struc[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.M_struc_sub, desired_M_struc_sub[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.C_struc, desired_C_struc[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.W_struc, desired_W_struc[index], rtol=1e-05, atol=1e-3)

    # Hydrostatic quantities
    assert_allclose(fowt.rCB, desired_rCB[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.C_hydro, desired_C_hydro[index], rtol=1e-05, atol=1e-3)
    assert_allclose(fowt.W_hydro, desired_W_hydro[index], rtol=1e-05, atol=1e-3)    


def test_hydroConstants(index_and_fowt):
    index, fowt = index_and_fowt
    fowt.calcHydroConstants() 
    assert_allclose(fowt.A_hydro_morison, desired_A_hydro_morison[index], rtol=1e-05, atol=1e-3)


def test_hydroExcitation(index_and_fowt):
    index, fowt = index_and_fowt    

    # Set this flag to true to replace the true values file
    flagSaveValues = False
    true_values_file = list_files[index].replace('.yaml', '_true_hydroExcitation.pkl')
    output_true_values = []
    
    list_wave_heading = [0, 45, 90, 135, 180, 225, 270, 315, 360]
    list_wave_period  = [5, 10, 15, 20]
    list_wave_height  = [1, 2]
    
    idxTrueValues = 0
    for wave_heading in list_wave_heading:
        for wave_period in list_wave_period:
            for wave_height in list_wave_height:
                # Create case dictionary. The other necessary fields have default values within calcHydroExcitation.
                # Using the default values is useful to check if they were changed.
                testCase = {'wave_heading': wave_heading, 'wave_period': wave_period, 'wave_height': wave_height}

                fowt.calcHydroConstants()
                fowt.calcHydroExcitation(testCase, memberList=fowt.memberList)

                if flagSaveValues:
                    output_true_values.append({
                        'case': testCase,
                        'w': fowt.w,
                        'F_hydro_iner': fowt.F_hydro_iner,
                    })
                else:
                    with open(true_values_file, 'rb') as f:
                        true_values = pickle.load(f)

                    assert_allclose(fowt.F_hydro_iner, true_values[idxTrueValues]['F_hydro_iner'], rtol=1e-05, atol=1e-3)                    
                idxTrueValues += 1

    if flagSaveValues:
        with open(true_values_file, 'wb') as f:
            pickle.dump(output_true_values, f)

def test_hydroLinearization(index_and_fowt):
    index, fowt = index_and_fowt

    # Set this flag to true to replace the true values file
    flagSaveValues = False
    true_values_file = list_files[index].replace('.yaml', '_true_hydroLinearization.pkl')

    testCase = {'wave_spectrum': 'unit', 'wave_heading': 0, 'wave_period': 10, 'wave_height': 2} # Currently we need to specify wave period and height, even though they are not used for unit spectrum
    fowt.calcHydroExcitation(testCase, memberList=fowt.memberList) # Need wave kinematics

    phase_array = np.linspace(0, 2 * np.pi, fowt.nw * 6).reshape(6, fowt.nw) # Needed an arbitrary motion amplitude. Assuming uniform amplitude with phases linearly spaced between 0 and 2pi. Times 6 for surge, sway, ..., yaw
    Xi = 0.1*np.exp(1j * phase_array)
    B_hydro_drag = fowt.calcHydroLinearization(Xi)   
    F_hydro_drag = fowt.calcDragExcitation(0)
    if flagSaveValues:
        with open(true_values_file, 'wb') as f:
            true_values = {'B_hydro_drag': B_hydro_drag, 'F_hydro_drag': F_hydro_drag}
            pickle.dump(true_values, f)
        return
    else:
        with open(true_values_file, 'rb') as f:
            true_values = pickle.load(f)

    # Check the linearized drag matrix
    assert_allclose(B_hydro_drag, true_values['B_hydro_drag'], rtol=1e-05, atol=1e-10)

    # Check the linearized drag excitation
    assert_allclose(F_hydro_drag, true_values['F_hydro_drag'], rtol=1e-05)

def test_calcCurrentLoads(index_and_fowt):
    index, fowt = index_and_fowt    
    testCase = {'current_speed': 2.0, 'current_heading':15}
    D = fowt.calcCurrentLoads(testCase)

    assert_allclose(D, desired_current_drag[index], rtol=1e-05, atol=1e-3)


'''
 To run as a script. Useful for debugging.
'''
if __name__ == "__main__":
    index = 0

    fowt = create_fowt(list_files[index])
    test_statics((index,fowt))
    
    fowt = create_fowt(list_files[index])
    test_hydroConstants((index,fowt))

    fowt = create_fowt(list_files[index])
    test_hydroExcitation((index,fowt))

    fowt = create_fowt(list_files[index])
    test_hydroLinearization((index,fowt))

    fowt = create_fowt(list_files[index])
    test_calcCurrentLoads((index,fowt))

