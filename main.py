from time import sleep
from maths import degrees
from body import init_servo, set_servo_angles
from maths import get_x_zmp, get_angles, PID_Controller, minmax
from sensor import ACCEL_out, GYRO_out, ADC_out
from math import radians

init_servo()

swing_leg, station_leg = ([degrees(x) for x in get_angles(-3, 9, 5, 5, 3)], [degrees(x) for x in get_angles(1, 9, 5, 5, 3)])

set_servo_angles(swing_leg, station_leg)

delay = 0.01
xl, xr = 0, 0
prev_e = 0
hip_integral = 0
knee_integral = 0

counter = 0
swing_change = True


perfect_zmp = 0
while True:
    _, acclx, acclz = ACCEL_out()
    fl, fr = ADC_out()
    x_zmp = get_x_zmp(fl, fr, xl, xr, acclx, acclz, 16, delay, 0.7)

    e = x_zmp
    hip_integral = minmax(hip_integral, n=-20, p=20)
    knee_integral = minmax(knee_integral, n=-20, p=20)
    delta_hip_angle, hip_integral = PID_Controller(0.3, 0.01, 0, e, prev_e, delay, hip_integral)
    prev_e = e

    swing_leg[0] = station_leg[0] = minmax(swing_leg[0] + delta_hip_angle)

    set_servo_angles(swing_leg, station_leg)
    sleep(delay)
