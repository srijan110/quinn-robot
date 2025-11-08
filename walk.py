from maths import degrees, get_coords, get_angles
from body import init_servo, set_servo_angles
from time import sleep

if __name__ != "__main__":
    exit()

# example test code

delay = 0.01
index = 0
total = round(0.25/delay)

init_servo()

swing = True

ix, iy = -3, 9
fx, fy = 1, 9

while True:
    x, y = get_coords(index, total, swing, ix, iy, fx, fy, -1)
    lx, ly = get_coords(index, total, not swing, fx, fy, ix, iy, -1)
    # print(x, y)
    set_servo_angles([degrees(x) for x in get_angles(x, y, 5, 5, 3)], [degrees(x) for x in get_angles(lx, ly, 5, 5, 3)])
    sleep(delay)
    index += 1
    if index >= total+1 or index == total+1:
        index = 0
        swing = not swing
        ix, iy, fx, fy = fx, fy, ix, iy
