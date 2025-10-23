from adafruit_servokit import ServoKit
from time import sleep
from math import sin, cos, radians, pi, acos, atan2, sqrt, degrees


def get_angles(x, y, l1, l2, l3):
    global state
    r = sqrt(x**2 + y**2)

    angle_hip = atan2(y, x)-acos((l1**2+r**2-l2**2)/(2*l1*r))
    angle_knee = pi-acos((l1**2 + l2**2 - r**2)/(2*l1*l2))

    angle_ankle = radians(0) - (angle_knee + angle_hip)

    return angle_hip, angle_knee, angle_ankle


def minmax(x, p=180, n=0):
    return min(p, max(x, n))


kit = ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(450, 2600)
kit.servo[1].set_pulse_width_range(450, 2600)
kit.servo[2].set_pulse_width_range(500, 2600)
kit.servo[3].set_pulse_width_range(450, 2500)
kit.servo[4].set_pulse_width_range(500, 2600)
kit.servo[5].set_pulse_width_range(500, 2600)


def set_servo_angles(leg_one, leg_two):
    kit.servo[0].angle = minmax(leg_one[0] - 5)  # 85
    kit.servo[1].angle = minmax(leg_two[0] + 5)  # 95
    kit.servo[2].angle = minmax(leg_one[1] + 90 - 5)  # 85
    kit.servo[3].angle = minmax(leg_two[1] + 90 - 5)  # 85
    kit.servo[4].angle = minmax(leg_one[2] + 180 + 5)  # 95
    kit.servo[5].angle = minmax(leg_two[2] + 180)  # 90


while True:
    leg_one = [
        degrees(x) for x in get_angles(-2, 9, 5, 5, 3)]

    leg_two = [
        degrees(x) for x in get_angles(3, 9, 5, 5, 3)]

    set_servo_angles(leg_one, leg_two)
    sleep(1)
    set_servo_angles(leg_two, leg_one)
    sleep(1)
