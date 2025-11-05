from time import sleep
from maths import degrees
from body import init_servo, set_servo_angles
from maths import get_x_zmp, get_angles, PID_Controller, minmax
from sensor import ACCEL_out, GYRO_out, ADC_out
from math import radians

init_servo()


leg_state = {
    "stationary_0": [degrees(x) for x in get_angles(2, 9, 5, 5, 3)],
    "stationary_1": [degrees(x) for x in get_angles(1, 9, 5, 5, 3)],
    "stationary_2": [degrees(x) for x in get_angles(0, 9, 5, 5, 3)],
    "stationary_3": [degrees(x) for x in get_angles(1, 9, 5, 5, 3)],
    "stationary_4": [degrees(x) for x in get_angles(-2, 9, 5, 5, 3)],
    "moving_0": [degrees(x) for x in get_angles(-2, 9, 5, 5, 3)],
    "moving_1": [degrees(x) for x in get_angles(-1, 8, 5, 5, 3)],
    "moving_2": [degrees(x) for x in get_angles(0, 8, 5, 5, 3)],
    "moving_3": [degrees(x) for x in get_angles(1, 9, 5, 5, 3)],
    "moving_4": [degrees(x) for x in get_angles(2, 9, 5, 5, 3)]
}

# leg_state["moving_1"][2] += 15
leg_one, leg_two = ([degrees(x) for x in get_angles(-3, 9, 5, 5, 3)], [degrees(x) for x in get_angles(-3, 9, 5, 5, 3)])

set_servo_angles(leg_one, leg_two)

print([degrees(x) for x in get_angles(-2, 9, 5, 5, 3)], [degrees(x) for x in get_angles(-2, 9, 5, 5, 3)])

delay = 0.01
xl, xr = -1, -1
prev_e = 0
hip_integral = 0
knee_integral = 0

perfect_zmp = 0
print(leg_one[2])
while True:
    _, acclx, acclz = ACCEL_out()
    fl, fr = ADC_out()
    x_zmp = get_x_zmp(fl, fr, xl, xr, acclx, acclz, 16, delay, 0.5)

    e = x_zmp
    hip_integral = minmax(hip_integral, n=-20, p=20)
    knee_integral = minmax(knee_integral, n=-20, p=20)
    delta_hip_angle, hip_integral = PID_Controller(0.3, 0.01, 0, e, prev_e, delay, hip_integral)
    prev_e = e

    # leg_one[2] = leg_two[2] = minmax(leg_one[2] - delta_ankle_angle, p=-60, n=-120)
    leg_one[0] = leg_two[0] = minmax(leg_one[0] + delta_hip_angle)

    # print(leg_one[2])
    set_servo_angles(leg_one, leg_two)
    sleep(delay)
    if leg_one[2] > -75 or leg_one[2] < -150:
        pass
