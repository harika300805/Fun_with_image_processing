import cv2
import numpy as np

def onTrack1(val): 
  global huelow 
  hueLow = val

def onTrack2(val): 
  global hueHigh 
  hueHigh = val

def onTrack3(val): 
  global satLow 
  satLow = val

def onTrack4(val):
  global satHigh 
  satHigh = val

def onTracks(val): 
  global vallow 
  vallow = val

def onTrack6(val): 
  global valHigh 
  valHigh = val
cv2.namedwindow('Trackbars')
cv2.resizeWindow('Trackbars',400,300)
hueLow = 0
hueHigh =0
satLow =0
satHigh = 0
vallow =0
valHigh = 0

cv2.createTrackbar('Hue low', 'Trackbars', 110, 179, on Track1) 
cv2.createTrackbar(' High', 'Trackbars', 150, 179, onTrack2)
cv2.createTrackbar('Sat low', 'Trackbars', 80, 255, on Track3)
cv2.createTrackbar('Sat High', 'Trackbars', 255, 255, on Track4)
cv2.createTrackbar('Val low', 'Trackbars', 134, 255, onTrack5)
cv2.createTrackbar('Val High', 'Trackbars', 255, 255, on Track6)

image cv2.imread('rgb.jpg')

while True:
 frameHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
 lowerBound = np.array([hueLow,satLow,valLow])
 upperBound = np.array([hueHigh,satHigh,valHigh])
 mask = cv2.inRange(frameHSV, lowerBound, upperBound)
 masked = cv2.bitwise_and(image,image,mask=mask)
 cv2.imshow('mask', mask)
 cv2.imshow('Ball', image)
 cv2.imshow('masked',masked)
 print("lowerBound: ", lowerBound)
 print("upperBound: ", upperBound)
 if cv2.waitKey(1) & 0xff == ord('q'): 
  break
cv2.destroyAllWindows()
