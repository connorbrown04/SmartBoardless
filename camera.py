import math
import cv2 
import numpy as np 
import struct
import pandas as pd
import threading
from pynput import mouse
#import ctypes  
gx = 0
gy = 0

prevX = 0
prevY = 0


running = True

pressed = False

def write_report(report):
    fd = open('/dev/hidg0', 'rb+')
    fd.write(report)

# def send_reports():
#     while(running):
#         s = struct.pack('<B?B2HB', 1, pressed, 1, gx, gy, 1)
#         write_report(s)


def on_click(x, y, button, pressed):
    if pressed:
        pressed = True
    else:
        pressed = False

#creates listener and sets it to its own thread
mouse_listener = mouse.Listener(on_click=on_click)

mouse_thread = threading.Thread(target=mouse_listener.start)

# report_thread = threading.Thread(target=send_reports)
mouse_thread.start()
# report_thread.start()


cap1 = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(0)

right = False
left = False

#hdc = ctypes.cdll.user32.GetDC(0)  # Get the device context of the entire screen
#dpi = ctypes.cdll.gdi32.GetDeviceCaps(hdc, 88)  # 88 corresponds to LOGPIXELSX (horizontal DPI)
#ctypes.cdll.user32.ReleaseDC(0, hdc)

lower_lime_green = np.array([35, 40, 40])
upper_lime_green = np.array([70, 255, 255])

lower_hot_pink = np.array([170, 50, 50])
upper_hot_pink = np.array([180, 255, 255])

lower_blue = np.array([90, 50, 50])
upper_blue = np.array([100, 255, 255])



#will run into a camera dies or q is pressed
while cap1.isOpened() and cap2.isOpened() and running:
    #takes input from both cameras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        break
    #sets them to HSV format
    hsv_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    #takes the mask with green
    gmask1 = cv2.inRange(hsv_frame1, lower_lime_green, upper_lime_green)
    gmask2 = cv2.inRange(hsv_frame2, lower_lime_green, upper_lime_green)
    #takes the mask with pink
    pmask1 = cv2.inRange(hsv_frame1, lower_hot_pink, upper_hot_pink)
    pmask2 = cv2.inRange(hsv_frame2, lower_hot_pink, upper_hot_pink)
    #takes the mask with blue
    bmask1 = cv2.inRange(hsv_frame1, lower_blue, upper_blue)
    bmask2 = cv2.inRange(hsv_frame2, lower_blue, upper_blue)
    


    def median(mask):
        frame = pd.DataFrame(mask)
        histogram = frame.sum()
        histogram.div(255)
        total = 0
        median_index = (histogram.sum() + 1) / 2
        for value in range(len(histogram)):
            total += histogram[value]
            if total > median_index:
                return value
        return 0
    
    
    gmedianX1 = median(gmask1)
    gradians1 = (gmedianX1-320)*45/320#*(math.pi/180)
    gmedianX2 = median(gmask2)
    gradians2 = ((gmedianX2-320)*45/320)#*(math.pi/180)
        
    pmedianX1 = median(pmask1)
    pradians1 = (pmedianX1-320)*45/320#*(math.pi/180)
    pmedianX2 = median(pmask2)
    pradians2 = ((pmedianX2-320)*45/320)#*(math.pi/180)
        
    bmedianX1 = median(bmask1)
    bradians1 = (bmedianX1-320)*45/320#*(math.pi/180)
    bmedianX2 = median(bmask2)
    bradians2 = ((bmedianX2-320)*45/320)#*(math.pi/180)  



    #finds which of the median radians are the closest together and averages them
    gpdiff1 = abs(gradians1-pradians1)
    gbdiff1 = abs(gradians1-bradians1)
    pbdiff1 = abs(pradians1-bradians1)
    diffmin1 = min(gbdiff1,gpdiff1,pbdiff1)
    if diffmin1 == gpdiff1:
        radians1 = (gradians1+pradians1)/2
    elif diffmin1 == gbdiff1:
        radians1 = (gradians1+bradians1)/2
    else:
        radians1 = (pradians1+bradians1)/2

    gpdiff2 = abs(gradians2-pradians2)
    gbdiff2 = abs(gradians2-bradians2)
    pbdiff2 = abs(pradians2-bradians2)
    diffmin2 = min(gbdiff2,gpdiff2,pbdiff2)
    if diffmin2 == gpdiff2:
        radians2 = (gradians2+pradians2)/2
    elif diffmin2 == gbdiff2:
        radians2 = (gradians2+bradians2)/2
    else:
        radians2 = (pradians2+bradians2)/2
    

    radians1 *= -(math.pi/180)
    radians2 *= -(math.pi/180)

    #uses the radians to determine x and y coordinates
    w = 100
    h = 100
    x = (math.tan(radians1)*w+h)/(math.tan(radians2+(math.pi/2))-math.tan(radians1))
    y = math.tan(radians1)*(x+w)

    x += 50
    y += 50

    if(x < 0): x = 0
    if(y < 0): y = 0

    x = (x/100)*16383
    y = 16383 - (y/100)*16383

    if(y < 0): y = 0

    



    x = math.floor((x + prevX)/4)
    y = math.floor((y + prevY)/4)

    gx = x
    gy = y

    # if(abs(x - prevX) > 1000 or abs(y - prevY) > 1000):
    #     x, y = prevX, prevY
    prevX, prevY = x, y

    s = struct.pack('<B?B2HB', 1, pressed, 1, gx, gy, 1)
    write_report(s) 
    


    # print(f"{x} , {y}")
    # gresult1 = cv2.bitwise_and(frame1, frame1, mask=gmask1)
    # gresult2 = cv2.bitwise_and(frame2, frame2, mask=gmask2)

    # presult1 = cv2.bitwise_and(frame1, frame1, mask=pmask1)
    # presult2 = cv2.bitwise_and(frame2, frame2, mask=pmask2)

    # bresult1 = cv2.bitwise_and(frame1, frame1, mask=bmask1)
    # bresult2 = cv2.bitwise_and(frame2, frame2, mask=bmask2)

    #shows the masks of the cameras
    # cv2.imshow('Original Frame1', frame1)
    # cv2.imshow('gmask1', gmask1)
    # cv2.imshow('pmask1', pmask1)
    # cv2.imshow('bmask1', bmask1)

    # cv2.imshow('Original Frame2', frame2)
    # cv2.imshow('gmask2', gmask2)
    # cv2.imshow('pmask2', pmask2)
    # cv2.imshow('bmask2', bmask2)



    


    #stops everything if q is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        running = False



