from math import sin, cos, radians, pi, acos, atan2, sqrt, degrees


def get_coords(index, total, curved, ix, iy, fx, fy, h):
    if not curved:
        diffx, diffy = fx - ix, fy - iy
        framex, framey = diffx / total, diffy / total
        return ix + framex * index, iy + framey * index

    else:
        x, y = cubic_bezier((ix, iy), (ix, iy+h), (fx, fy+h), (fx, fy), index/total)
        return x, y


def cubic_bezier(p0, p1, p2, p3, t):
    u = 1 - t
    x = (u**3)*p0[0] + 3*(u**2)*t*p1[0] + 3*u*(t**2)*p2[0] + (t**3)*p3[0]
    y = (u**3)*p0[1] + 3*(u**2)*t*p1[1] + 3*u*(t**2)*p2[1] + (t**3)*p3[1]
    return x, y


def get_angles(x, y, l1, l2, l3):
    global state
    r = sqrt(x**2 + y**2)

    angle_hip = atan2(y, x)-acos((l1**2+r**2-l2**2)/(2*l1*r))
    angle_knee = pi-acos((l1**2 + l2**2 - r**2)/(2*l1*l2))

    angle_ankle = radians(0) - (angle_knee + angle_hip)

    return angle_hip, angle_knee, angle_ankle


def minmax(x, p=180, n=0):
    return min(p, max(x, n))


def get_x_zmp(fl, fr, xl, xr, ax, ux, z_c, dt, alpha):
    xcom = ux * dt + 0.5 * ax * dt * dt

    xzmp_imu = xcom - (z_c / 9.8) * ax
    xzmp_fsr = (xl*fl + xr*fr)/minmax(fl+fr, n=0.01)

    return (alpha * xzmp_fsr) + ((1 - alpha) * xzmp_imu)


def PID_Controller(kp, ki, kd, e, prev_e, dt, prev_integral):
    integral = prev_integral + e * dt
    return kp * e + kd * (e - prev_e) / dt + ki * integral, integral


if __name__ == "__main__":
    print(get_x_zmp(1, 1, 0, 0, 0, 0, 16, 0.1, 0.6))
