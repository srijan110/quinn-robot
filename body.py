from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)


def minmax(x, p=180, n=0):
    return min(p, max(x, n))


def init_servo():
    kit.servo[0].set_pulse_width_range(450, 2600)
    kit.servo[1].set_pulse_width_range(450, 2600)
    kit.servo[2].set_pulse_width_range(500, 2500)
    kit.servo[3].set_pulse_width_range(450, 2500)
    kit.servo[4].set_pulse_width_range(500, 2600)
    kit.servo[5].set_pulse_width_range(500, 2600)


def set_hip_servo_angles(hip):
    kit.servo[6].angle = minmax(hip[0])
    kit.servo[7].angle = minmax(hip[1])


def set_leg_servo_angles(leg_one, leg_two):
    kit.servo[0].angle = minmax(leg_one[0] + 10)  # 85
    kit.servo[1].angle = minmax(leg_two[0])  # 95
    kit.servo[2].angle = minmax(leg_one[1] + 90 + 10)  # 85
    kit.servo[3].angle = minmax(leg_two[1] + 90 - 10)  # 85
    kit.servo[4].angle = minmax(leg_one[2] + 180 - 7, n=60, p=120)  # 95
    kit.servo[5].angle = minmax(leg_two[2] + 180 + 8, n=60, p=120)  # 90
