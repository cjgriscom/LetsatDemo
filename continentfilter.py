
import cv2
import numpy as np

def getContinentFilter(img):
  
  img = cv2.blur(img.copy(),(3,3))
  
  imgHSV = cv2.cvtColor(img,  cv2.COLOR_RGB2HSV)


  (thresh, im_bw) = cv2.threshold(imgHSV[:,:,0], 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

  return cv2.cvtColor(im_bw, cv2.COLOR_GRAY2RGB)
