from time import sleep
from maths import degrees
from body import init_servo, set_servo_angles
from maths import get_x_zmp, get_angles, PID_Controller, minmax, get_coords
from sensor import ACCEL_out, GYRO_out, ADC_out
from math import radians


def walk_front(ix=1, iy=9, fx=-2, fy=9, hip_offset=-10, ankle_offset=0, step_duration=0.2, delay=0.01, dx=-1, dy=9, steps=1):
    left_leg, right_leg = ([degrees(x) for x in get_angles(dx, dy, 5, 5, 3)], [degrees(x) for x in get_angles(-1, 9, 5, 5, 3)])
    left_leg[0] = right_leg[0] = left_leg[0] + hip_offset
    set_servo_angles(left_leg, right_leg)

    index = 0
    total = round(step_duration/delay)
    swing = True

    step_index = 0
    sleep(delay)

    while step_index != steps:
        lx, ly = get_coords(index, total, swing, ix, iy, fx, fy, -2)
        rx, ry = get_coords(index, total, not swing, fx, fy, ix, iy, -2)

        left_leg = [degrees(x) for x in get_angles(lx, ly, 5, 5, 3)]
        right_leg = [degrees(x) for x in get_angles(rx, ry, 5, 5, 3)]

        print(left_leg)

        left_leg[0] = minmax(left_leg[0] + hip_offset - 15)
        right_leg[0] = minmax(right_leg[0] + hip_offset - 15)

        set_servo_angles(left_leg, right_leg)
        sleep(delay)

        index += 1
        if index >= total+1 or index == total+1:
            index = 0
            step_index += 1
            swing = not swing
            ix, iy, fx, fy = fx, fy, ix, iy

    left_leg, right_leg = ([degrees(x) for x in get_angles(dx, dy, 5, 5, 3)], [degrees(x) for x in get_angles(-1, 9, 5, 5, 3)])
    left_leg[0] = right_leg[0] = left_leg[0] + hip_offset
    set_servo_angles(left_leg, right_leg)


if __name__ == "__main__":
    init_servo()

    walk_front(steps=50)
