# -*- coding: UTF-8 -*-
import time
import cv2
import numpy as np
import pyzbar.pyzbar as zbar


import RPi.GPIO as GPIO


 # 规定GPIO引脚
IN1 = 18      # 接PUL-
IN2 = 16      # 接PUL+
IN3 = 15      # 接DIR-
IN4 = 13      # 接DIR+
 
def setStep(w1, w2, w3, w4):
    GPIO.output(IN1, w1)
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)
 
def stop():
    setStep(0, 0, 0, 0)
 
def forward(delay, steps):  
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
 
def backward(delay, steps):  
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
 
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(IN1, GPIO.OUT)      # Set pin's mode is output
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
 
def loop():
    while True:
        print ("backward...")
        backward(0.001, 1000)   # 发射脉冲时间间隔0.0001（单位秒）   脉冲个数1000
        
        print ("stop...")
        stop()                 # stop
        time.sleep(3)          # sleep 3s
        
        print ("forward...")
        forward(0.001, 1000)
        
        print ("stop...")
        stop()
        time.sleep(3)


def position1():
    forward(0.003,100)
    stop()
    time.sleep(5)
def back1():
    backward(0.003,100)
    stop()
    time.sleep(2)
def position2():
    backward(0.003,140)
    stop()
    time.sleep(5)
def back2():
    forward(0.003,140)
    stop()
    time.sleep(2)
def position3():
    backward(0.003,265)
    stop()
    time.sleep(5)
def back3():
    forward(0.003,265)
    stop()
    time.sleep(2)
def destroy():
    GPIO.cleanup()             # 释放数据
 

    

if __name__ == '__main__':

    font = cv2.FONT_HERSHEY_SIMPLEX
    # 如果你使用USB接口的摄像头，参数改为 1
    cap = cv2.VideoCapture(1)
    cap.set(3, 960)
    cap.set(4, 720)
    if (not cap.isOpened()):
        print("无法打开该摄像头！")
    while (True):
        ret, img = cap.read()
        img_ROI_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        barcodes = zbar.decode(img_ROI_gray)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(img, text, (20, 100), font, 1, (0, 255, 0), 4)
            print("[INFO] Found {} QRcode/barcode: {}".format(barcodeType, barcodeData))
            print(text[0:4])
            str1 = '6954'
            str2 = '6934'
            
            if(int(text[0:4]) == 6954):
                print("Case 1")
                setup()
                try:
                    position1()
                    back1()
                except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
                    destroy()
            if(int(text[0:4]) == 6925):
                print("Case 2")
                setup()
                try:
                    position2()
                    back2()
                except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
                    destroy()
            if(int(text[0:4]) == 6906):
                print("Case 3")
                setup()
                try:
                    position3()
                    back3()
    
                except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child function destroy() will be  executed.
                    destroy()
        
        if (cv2.waitKey(1)) == ord('q'):
            break
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()

