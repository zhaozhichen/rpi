import cv2
import numpy as np
AREA_CUTOFF_THRESHOLD = 0.5
filename='images/test.jpg'

# Adjust card orientation
def rectify(h):
  h = h.reshape((4,2))
  hnew = np.zeros((4,2),dtype = np.float32)
  add = h.sum(1)
  hnew[3] = h[np.argmin(add)]
  hnew[1] = h[np.argmax(add)]
  diff = np.diff(h,axis = 1)
  hnew[0] = h[np.argmin(diff)]
  hnew[2] = h[np.argmax(diff)]
  return hnew

# Image Matching
def preprocess(img):
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(5,5),0)
  thresh = cv2.adaptiveThreshold(blur,255,1,1,11,1)
  return thresh

def imgdiff(img1,img2):
  diffAll=0
  for i in range(3): # channel BGR
    img1 = cv2.GaussianBlur(img1[:,:,i],(5,5),0)
    img2 = cv2.GaussianBlur(img2[:,:,i],(5,5),0)
    diff = cv2.absdiff(img1,img2)
    diff = cv2.GaussianBlur(diff,(5,5),5)
    flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY)
    diffAll += np.sum(diff)
  return diffAll

def find_closest_card(training,img):
  features = preprocess(img)
  return sorted(training.values(), key=lambda x:imgdiff(x,features))[0][0]


im = cv2.imread(filename)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),1000)
flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
#thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
lastArea = cv2.contourArea(contours[0])
for i,card in enumerate(contours):
    peri = cv2.arcLength(card,True)
    approx = cv2.approxPolyDP(card,0.02*peri,True)
    if approx.shape!=(4,1,2):
        continue
    approx = rectify(approx)
    newArea = cv2.contourArea(card)
    if newArea<lastArea * AREA_CUTOFF_THRESHOLD:
        break
    lastArea = newArea
    approx2 = np.array(approx.reshape((4,2)),np.float32)
    # rect = cv2.minAreaRect(contours[2])
    # r = cv2.boxPoints(rect)
    h = np.array([ [0,0],[299,0],[299,449],[0,449] ],np.float32)
    transform = cv2.getPerspectiveTransform(approx2,h)
    warp = cv2.warpPerspective(im,transform,(300,450))
    savefile = "images/decomp"+str(i)+".jpg"
    cv2.imwrite(savefile,warp)
