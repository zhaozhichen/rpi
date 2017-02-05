import cv2
import numpy as np

# Adjust card orientation
def rectify(hIn):
    hIn = hIn.reshape((4,2))
    hOut = np.zeros((4,2),dtype = np.float32)
    add = hIn.sum(1)
    hOut[0] = hIn[np.argmin(add)]
    hOut[2] = hIn[np.argmax(add)]
    diff = np.diff(hIn,axis = 1)
    hOut[1] = hIn[np.argmin(diff)]
    hOut[3] = hIn[np.argmax(diff)]
    return hOut

# rotate card by 90 degree
def rotate(hIn):
    hOut = np.zeros((4,2),dtype = np.float32)
    hOut[0] = hIn[1]
    hOut[1] = hIn[2]
    hOut[2] = hIn[3]
    hOut[3] = hIn[0]
    return hOut

# calc lenth square between two points
def lenSq(pt1,pt2):
    x=pt2[0]-pt1[0]
    y=pt2[1]-pt1[1]
    return x*x+y*y

def cutEdge(imgIn, pixel):
    (lenth,width,depth) = imgIn.shape
    imgOut = np.zeros((lenth-pixel*2,width-pixel*2,depth))
    for i in range(lenth-pixel*2):
        for j in range(width-pixel*2):
            for k in range(depth):
                imgOut[i,j,k] = imgIn[i+pixel,j+pixel,k]
    return imgOut

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

def getCards(imgfile):
    im = cv2.imread(imgfile)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray,(1,1),0)
    flag, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    im2, contours, hierarchy = \
        cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    lastArea = cv2.contourArea(contours[0])
    resCards=[]
    for i,card in enumerate(contours):
        peri = cv2.arcLength(card,True)
        approx = cv2.approxPolyDP(card,0.02*peri,True)
        if approx.shape!=(4,1,2):
            continue
        rect = rectify(approx)
        if lenSq(rect[1],rect[0])>peri*peri/16:
            rect=rotate(rect)
        newArea = cv2.contourArea(card)
        if newArea<lastArea * 0.5:
            break
        lastArea = newArea
        # approx2 = np.array(rect.reshape((4,2)),np.float32)
        # rect = cv2.minAreaRect(contours[2])
        # r = cv2.boxPoints(rect)
        h = np.array([ [0,0],[290,0],[290,449],[0,449] ],np.float32)
        transform = cv2.getPerspectiveTransform(rect,h)
        warp = cv2.warpPerspective(im,transform,(290,450))
        resCards.append(warp)
    return resCards
        #warp = cutEdge(warp,5)
        #savefile = "images/decomp"+str(i)+".jpg"
        #cv2.imwrite(savefile,warp)

def train(trainSet):
    resTrain = []
    for trainImg in trainSet:
        resTrain+=getCards(trainImg)
    return resTrain
