# -*- coding: UTF-8 -*-
import time
import cv2
import numpy as np
import pyzbar.pyzbar as zbar

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
            if(int(text[0:4]) == 6925):
                print("Case 2")
            if(int(text[0:4]) == 6906):
                print("Case 3")
        cv2.imshow('image', img)
        
        if (cv2.waitKey(1)) == ord('q'):
            break
        time.sleep(0.5)
    cap.release()
    cv2.destroyAllWindows()
