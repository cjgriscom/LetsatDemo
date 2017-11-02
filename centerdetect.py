
import cv2
import numpy as np

def getEllipseImg(img):
  # Gray
  img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

  # Blur
  #img_blur = img_gray
  img_blur = cv2.medianBlur(img_gray,5)

  #img_sharp = img_blur
  # Local contrast using some linear algebra that I don't understand
  kernel = np.array([[-1,-1,-1], [-1,20,-1], [-1,-1,-1]])
  img_sharp = cv2.filter2D(img_blur, -1, kernel)
  # End


  _, img_sharp = cv2.threshold(img_sharp, 50,255,0)
  img_gaus1 = cv2.blur(img_sharp, (3,3))
  img_gaus2 = cv2.blur(img_sharp, (5,5))
  img_edge = img_gaus1 ^ img_gaus2
  # Produce edge bitmap
  #img_edge = cv2.Canny(img_sharp, 50, 100,apertureSize=3)
  # End

  # Find largest contours
  _, contours, hierarchy = cv2.findContours(img_edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE ); # Find contours

  imgC = cv2.cvtColor(img_sharp, cv2.COLOR_GRAY2RGB)

  largestCircle = 0
  largestArea = 0
  maxLen = 0
  largestContour = []
  for contour in contours:
      arclen = cv2.arcLength(contour, 0)
      a=cv2.contourArea(contour)
      if arclen>6:
          #ellipse = cv2.fitEllipse(contour)
          minEC = cv2.minEnclosingCircle( contour );
          #print minEC
          #print ellipse
          if minEC[1] > largestCircle and arclen > maxLen and a > largestArea:
              imgC = cv2.drawContours(imgC,[contour] ,0,(0,255,0),3)
              largestCircle=minEC[1];
              largestArea = a
              largestContour = contour
              maxLen = arclen
              print minEC
  #imgC = cv2.drawContours(imgC,[largestContour] ,0,(255,0,0),3)
  ellipse = cv2.fitEllipse(largestContour)
  imgE = cv2.ellipse(img.copy(),ellipse,(0,255,0),3)
  cv2.circle(imgE,(np.uint16(ellipse[0][0]), np.uint16(ellipse[0][1])),2,(0,0,255),3)
  print ellipse
  return imgE
