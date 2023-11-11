# importing libraries 
import cv2 
import numpy as np 
  
cap = cv2.VideoCapture(0) 
lowerGreen = np.array([0,80,60]) #in hsv
upperGreen = np.array([240,100,100]) 
while(cap.isOpened()): 
      
    ret, frame = cap.read() 
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(framehsv, lowerGreen, upperGreen)
    cv2.imshow('Original', frame)
    cv2.imshow('HSV', framehsv)
    cv2.imshow('Mask', mask)   
    if cv2.waitKey(25) & 0xFF == ord('q'): 
        break 

cap.release() 
cv2.destroyAllWindows()