import math
import cv2 
import numpy as np 
import struct
#import ctypes  

def write_report(report):
    fd = open('/dev/hidg0', 'rb+')
    fd.write(report)


cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

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
while cap1.isOpened() and cap2.isOpened():
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
    #gets the median radian of the green mask
    gmaskCoords1 = np.column_stack(np.where(gmask1 > 0))
    gmaskCoords2 = np.column_stack(np.where(gmask2 > 0))
    if(len(gmaskCoords1) > 0):
        gmedianX1 = -(gmaskCoords1[math.floor(len(gmaskCoords1)/2)][1]-300)
        gradians1 = gmedianX1*45/300*(math.pi/180)
    
    if(len(gmaskCoords2) > 0):
        gmedianX2 = -(gmaskCoords2[math.floor(len(gmaskCoords2)/2)][1]-300)
        gradians2 = (gmedianX2*45/300)*(math.pi/180)
    

    #gets the median radian of the pink mask
    pmaskCoords1 = np.column_stack(np.where(pmask1 > 0))
    pmaskCoords2 = np.column_stack(np.where(pmask2 > 0))
    if(len(pmaskCoords1) > 0):
        pmedianX1 = -(pmaskCoords1[math.floor(len(pmaskCoords1)/2)][1]-300)
        pradians1 = pmedianX1*45/300*(math.pi/180)
    
    if(len(pmaskCoords2) > 0):
        pmedianX2 = -(pmaskCoords2[math.floor(len(pmaskCoords2)/2)][1]-300)
        pradians2 = (pmedianX2*45/300)*(math.pi/180)


    #gets the median radian of the blue mask
    bmaskCoords1 = np.column_stack(np.where(bmask1 > 0))
    bmaskCoords2 = np.column_stack(np.where(bmask2 > 0))
    if(len(bmaskCoords1) > 0):
        bmedianX1 = -(bmaskCoords1[math.floor(len(bmaskCoords1)/2)][1]-300)
        bradians1 = bmedianX1*45/300*(math.pi/180)
    
    if(len(bmaskCoords2) > 0):
        bmedianX2 = -(bmaskCoords2[math.floor(len(bmaskCoords2)/2)][1]-300)
        bradians2 = (bmedianX2*45/300)*(math.pi/180)

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
    diffmin2 = min(gbdiff1,gpdiff1,pbdiff1)
    if diffmin2 == gpdiff2:
        radians2 = (gradians2+pradians2)/2
    elif diffmin2 == gbdiff2:
        radians2 = (gradians2+bradians2)/2
    else:
        radians2 = (pradians2+bradians2)/2
    
    #uses the radians to determine x and y coordinates
    w = 100
    h = 100
    x = (math.tan(radians1)*w+h)/(math.tan(radians2+(math.pi/2)))-math.tan(radians1)
    y = math.tan(radians1)*(x+w)
    
    if x < -50:
        x = -50
    if x > 50:
        x = 50
    if y < -50:
        y = -50
    if y > 50:
        y = 50
    
    x += 50
    y += 50
    
    x = math.floor((x/100)*4095)
    y = math.floor((y/100)*4095)


    # s = struct.pack('<B?B2HB', 1, True, 1, x, y, 1)
    # write_report(s)


    print(f"{x} , {y}")
    # gresult1 = cv2.bitwise_and(frame1, frame1, mask=gmask1)
    # gresult2 = cv2.bitwise_and(frame2, frame2, mask=gmask2)

    # presult1 = cv2.bitwise_and(frame1, frame1, mask=pmask1)
    # presult2 = cv2.bitwise_and(frame2, frame2, mask=pmask2)

    # bresult1 = cv2.bitwise_and(frame1, frame1, mask=bmask1)
    # bresult2 = cv2.bitwise_and(frame2, frame2, mask=bmask2)

    #shows the masks of the cameras
    # cv2.imshow('Original Frame1', frame1)
    # cv2.imshow('gResult1', gresult1)
    # cv2.imshow('pResult1', presult1)
    # cv2.imshow('bResult1', bresult1)

    # cv2.imshow('Original Frame2', frame2)
    # cv2.imshow('gResult2', gresult2)
    # cv2.imshow('pResult2', presult2)
    # cv2.imshow('bResult2', bresult2)
    #stops everything if q is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


