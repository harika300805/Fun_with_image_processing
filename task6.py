import cv2
import numpy as np
val = 0
def trackbar_1(value):
 global val 
 val = value
 print('Value: ',val)
cv2.namedWindow('Trackbars')
cv2.resizeWindow('Trackbars',500,50)
cv2.createTrackbar('Value','Trackbars',val,100,trackbar_1)
cv2.waitKey()
cv2.destroyAllWindows()
