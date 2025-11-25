from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15
import board
import adafruit_mpu6050
from maths import minmax

def init_sensor():
    i2c = board.I2C()
    ads = ADS1015(i2c)
    ads.gain = ads.gains[2]
    mpu = adafruit_mpu6050.MPU6050(i2c)


def ADC_out():
    chan1 = AnalogIn(ads, ads1x15.Pin.A0)
    chan2 = AnalogIn(ads, ads1x15.Pin.A1)

    return round(minmax(chan1.value, p=22000)/22000, 3), round(minmax(chan2.value, p=22000)/22000, 3)


def GYRO_out():
    return mpu.gyro


def ACCEL_out():
    global mpu
    try:
        return mpu.acceleration
    except:
        mpu = adafruit_mpu6050.MPU6050(i2c)
        return mpu.acceleration


if __name__ == "__main__":
    print(ADC_out())
    print(GYRO_out())
    print(ACCEL_out())
