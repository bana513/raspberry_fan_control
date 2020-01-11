import RPi.GPIO as GPIO
import time
import os
import json
import sys


def get_temp():
    # You should run this as administrator
    temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").readlines()
    temp = temp[0]
    temp = float(temp)
    temp = temp / 1000
    return temp


def duty_cycle(temp, targets):
    pwm = 0
    for t, target in targets:
        if temp > t:
            pwm = max(pwm, target)
    return min(100, pwm)


if __name__ == "__main__":
    if len(sys.argv) <= 1: config_file = "config.json"
    else: config_file = sys.argv[1]

    with open(config_file) as json_file:
        config = json.load(json_file)
    print(config)

    use_pwm = config.get('use_pwm', False)
    refresh_interval = config.get('refresh_interval', 3)
    pwm_freq = config.get('pwm_freq', 300000)
    pwm_temp = config.get('pwm_temp', None)
    if pwm_temp is None: use_pwm = False

    try:
        fan_pin = config['fan_pin']
    except KeyError:
        exit(1)

    if use_pwm:
        targets = pwm_temp.get('targets', [])
    else:
        non_pwm_temp = config.get('non_pwm_temp', None)
        temp_on = 65 if non_pwm_temp is None else non_pwm_temp.get('temp_on', 65)
        temp_off = 60 if non_pwm_temp is None else non_pwm_temp.get('temp_off', 60)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(fan_pin, GPIO.OUT)

    if use_pwm:
        fan = GPIO.PWM(fan_pin, pwm_freq)

    try:
        while True:
            temp = get_temp()

            if use_pwm:
                pwm = duty_cycle(temp, targets)
                fan.start(pwm)
            else:
                if temp > temp_on:
                    pwm = 100
                    GPIO.output(fan_pin, GPIO.HIGH)
                elif temp < temp_off:
                    pwm = 0
                    GPIO.output(fan_pin, GPIO.LOW)

            print("CPU temp: {0:.1f}C, fan: {1}%".format(temp, pwm))
            time.sleep(refresh_interval)

    except (KeyboardInterrupt, SystemExit):
        if use_pwm:
            fan.stop()
        else:
            GPIO.output(fan_pin, GPIO.LOW)
        GPIO.cleanup()
