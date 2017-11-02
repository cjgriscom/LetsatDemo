import sys
import cv2
import numpy as np
import time
from centerdetect import  *
from cloudfilter import  *
from continentfilter import  *
 
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('timelapse_cut2.mp4')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")


mode = 0
count = 0
# Read until video is completed
while(cap.isOpened()): 
  # Capture frame-by-frame
  ret, frame = cap.read()
  framenum = cap.get(cv2.CAP_PROP_POS_FRAMES)
  if ret == True:
    frame = frame[80:1000, 510:1410] 
    count += 1
    if framenum >= 500 and framenum <= 600:
      cap.set(cv2.CAP_PROP_POS_FRAMES, 600)
      continue
    elif framenum >= 1809:
      cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop
    if count % 50 == 0:
      mode = (mode + 1) % 4
    if count % 3 != 0:
      continue
    time.sleep(0.25)
    print count, " ", framenum
    # Display the resulting frame
    if mode == 0:
      img = getEllipseImg(frame)
      img = cv2.putText(img, "Center Detection", (30,30), 
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200,200,250), 1, cv2.LINE_AA);
    if mode == 1:
      clouds = getCloudFilter(frame)
      img = cv2.addWeighted(frame,1,clouds,-0.4,0)
      img = cv2.putText(img, "Cloud Filtering", (30,30), 
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200,200,250), 1, cv2.LINE_AA);
    if mode == 2:
      img = getContinentFilter(frame)
      img = cv2.putText(img, "Continent Detection", (30,30), 
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200,200,250), 1, cv2.LINE_AA);
    if mode == 3:
      clouds = cv2.blur(getContinentFilter(frame),(9,9))
      img = cv2.addWeighted(frame,1,clouds,-0.25,0)
      img = cv2.putText(img, "Continent Detection", (30,30), 
        cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8, (200,200,250), 1, cv2.LINE_AA);
      
    cv2.imshow('LetSat Live Imaging Demo',img)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()

