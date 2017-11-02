
import cv2
import numpy as np

def getCloudFilter(img):
  
  img = cv2.medianBlur(img.copy(),3)
    
  lowerSpace1 = np.array([15, 13, 14], dtype = "uint8")
  upperSpace1 = np.array([170, 150, 150], dtype = "uint8")

  mask1 = cv2.inRange(img, lowerSpace1, upperSpace1)
  mask = mask1# | mask2

  return cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
