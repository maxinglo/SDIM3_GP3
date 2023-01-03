import RPi.GPIO as GPIO
import time

# 接线顺序“橙对pins里的第一个，黄2，粉3，蓝4 红接l298n上的5v”
GPIO.setmode(GPIO.BOARD)
pins = [1, 2, 3, 4]
# 此处填写要用的引脚
reduction = 64
# 此处定义电机减速比
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
CCW = [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]]
CW = [[1, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1], [0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0]]
# 此处定义正反转相序


def rotate(step_delay: float, total_time: float, rotation: bool):
    #第一个参数步间延时，第二个参数总运动时间，第三个参数顺逆时针转动（True为逆时针）
    #实现流程：1.求要走几步。2.是否正反转。3.根据相序表走到步数用完。
    times = total_time/step_delay
    if rotation:
        temp = CCW
    else:
        temp = CW
    while times > 0:
        for key in temp:
            step(key)
            times = times - 1
            time.sleep(step_delay)
            if(times <= 0):
                return
    return


def step(key):
    i = 0
    for signal in key:
        if signal == 0:
            GPIO.output(i, GPIO.LOW)
            i = i + 1
        else:
            GPIO.output(i, GPIO.HIGH)
            i = i + 1
    return


GPIO.cleanup()
