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


def get_x_zmp(fl, fr, xl, xr, ax, ux, z_c, dt, alpha):
    xcom = ux * dt + 0.5 * ax * dt * dt

    xzmp_imu = xcom - (z_c / 9.8) * ax
    xzmp_fsr = (xl*fl + xr*fr)/(fl+fr)

    return (alpha * xzmp_fsr) + ((1 - alpha) * xzmp_imu)


def PD_Controller(kp, kd, e, prev_e, dt): 
    return kp * e + kd * (e - prev_e) / dt
