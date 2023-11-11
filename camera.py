import math
import cv2 
import numpy as np 
import ctypes

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(2)

hdc = ctypes.windll.user32.GetDC(0)  # Get the device context of the entire screen
dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 corresponds to LOGPIXELSX (horizontal DPI)
ctypes.windll.user32.ReleaseDC(0, hdc)

# Define the color range for lime green in HSV
lower_lime_green = np.array([40, 40, 40])
upper_lime_green = np.array([80, 255, 255])

lower_hot_pink = np.array([160, 50, 50])
upper_hot_pink = np.array([190, 255, 255])

lower_blue = np.array([10, 50, 50])
upper_blue = np.array([15, 255, 255])


while cap1.isOpened() and cap2.isOpened():
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        break

    hsv_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    gmask1 = cv2.inRange(hsv_frame1, lower_lime_green, upper_lime_green)
    gmask2 = cv2.inRange(hsv_frame2, lower_lime_green, upper_lime_green)

    pmask1 = cv2.inRange(hsv_frame1, lower_hot_pink, upper_hot_pink)
    pmask2 = cv2.inRange(hsv_frame2, lower_hot_pink, upper_hot_pink)

    bmask1 = cv2.inRange(hsv_frame1, lower_blue, upper_blue)
    bmask2 = cv2.inRange(hsv_frame2, lower_blue, upper_blue)

    gmaskCoords1 = np.column_stack(np.where(gmask1 > 0))
    gmaskCoords2 = np.column_stack(np.where(gmask2 > 0))
    if(len(gmaskCoords1) > 0):
        gmedianX1 = -(gmaskCoords1[math.floor(len(gmaskCoords1)/2)][1]-300)
        gradians1 = gmedianX1*45/300*(math.pi/180)
    
    if(len(gmaskCoords2) > 0):
        gmedianX2 = -(gmaskCoords2[math.floor(len(gmaskCoords2)/2)][1]-300)
        gradians2 = (gmedianX2*45/300)*(math.pi/180)
    


    pmaskCoords1 = np.column_stack(np.where(pmask1 > 0))
    pmaskCoords2 = np.column_stack(np.where(pmask2 > 0))
    if(len(pmaskCoords1) > 0):
        pmedianX1 = -(pmaskCoords1[math.floor(len(pmaskCoords1)/2)][1]-300)
        pradians1 = pmedianX1*45/300*(math.pi/180)
    
    if(len(pmaskCoords2) > 0):
        pmedianX2 = -(pmaskCoords2[math.floor(len(pmaskCoords2)/2)][1]-300)
        pradians2 = (pmedianX2*45/300)*(math.pi/180)



    bmaskCoords1 = np.column_stack(np.where(bmask1 > 0))
    bmaskCoords2 = np.column_stack(np.where(bmask2 > 0))
    if(len(bmaskCoords1) > 0):
        bmedianX1 = -(bmaskCoords1[math.floor(len(bmaskCoords1)/2)][1]-300)
        bradians1 = bmedianX1*45/300*(math.pi/180)
    
    if(len(bmaskCoords2) > 0):
        bmedianX2 = -(bmaskCoords2[math.floor(len(bmaskCoords2)/2)][1]-300)
        bradians2 = (bmedianX2*45/300)*(math.pi/180)

    #print(f"1: {radians1} 2: {radians2}")

    w = 100
    h = 100
    x = (math.tan(gradians1)*w+h)/(math.tan(gradians2+(math.pi/2)))-math.tan(gradians1)
    y = math.tan(gradians1)*(x+w)
    
    print(f"{x} , {y}")
    # Apply the mask to the frame
    gresult1 = cv2.bitwise_and(frame1, frame1, mask=gmask1)
    gresult2 = cv2.bitwise_and(frame2, frame2, mask=gmask2)

    presult1 = cv2.bitwise_and(frame1, frame1, mask=pmask1)
    presult2 = cv2.bitwise_and(frame2, frame2, mask=pmask2)

    bresult1 = cv2.bitwise_and(frame1, frame1, mask=bmask1)
    bresult2 = cv2.bitwise_and(frame2, frame2, mask=bmask2)

    # Display the original frame and the result
    cv2.imshow('Original Frame1', frame1)
    cv2.imshow('gResult1', gresult1)
    cv2.imshow('pResult1', presult1)
    cv2.imshow('bResult1', bresult1)

    cv2.imshow('Original Frame2', frame2)
    cv2.imshow('gResult2', gresult2)
    cv2.imshow('pResult2', presult2)
    cv2.imshow('bResult2', bresult2)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release

"""
cap = cv2.VideoCapture(0) 
lowerGreen = np.array([0,200,0]) 
upperGreen = np.array([50,255,50]) 
while(cap.isOpened()): 
      
    ret, frame = cap.read() 

    mask = cv2.inRange(frame, lowerGreen, upperGreen)
    cv2.imshow('Original', frame)

    cv2.imshow('Mask', mask)   
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break 

cap.release() 
cv2.destroyAllWindows()
"""