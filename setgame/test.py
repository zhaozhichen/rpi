import cv2
import numpy as np
numcards=9
filename='test.jpg'
im = cv2.imread(filename)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),1000)
flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]
for i in range(numcards):
  card = contours[i]
  peri = cv2.arcLength(card,True)
  approx = cv2.approxPolyDP(card,0.02*peri,True)
  rect = cv2.minAreaRect(contours[2])
  r = cv2.boxPoints(rect)
h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)
transform = cv2.getPerspectiveTransform(approx,h)
warp = cv2.warpPerspective(im,transform,(450,450))
