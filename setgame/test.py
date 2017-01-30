import cv2
import numpy as np
filename='test2.jpg'
im = cv2.imread(filename)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),1000)
flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
for i,card in enumerate(contours):
    peri = cv2.arcLength(card,True)
    approx = cv2.approxPolyDP(card,0.02*peri,True)
    if approx.shape!=(4,1,2):
        continue
    approx2 = np.array(approx.reshape((4,2)),np.float32)
    # rect = cv2.minAreaRect(contours[2])
    # r = cv2.boxPoints(rect)
    h = np.array([ [0,0],[299,0],[299,449],[0,449] ],np.float32)
    transform = cv2.getPerspectiveTransform(approx2,h)
    warp = cv2.warpPerspective(im,transform,(300,450))
    savefile = "decomp"+str(i)+".jpg"
    cv2.imwrite(savefile,warp)
