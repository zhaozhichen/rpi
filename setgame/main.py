import cv2
import numpy as np
from setgameLib import *
trainSet = ['train/'+str(i)+'.jpg' for i in range(9)]

trainCards = train(trainSet)

print "training complete"

res=[]
for i, card in enumerate(train(['test.jpg'])):
    cv2.imwrite('test'+str(i)+'.jpg',card)
    r=[]
    for trainCard in trainCards:
        r.append(imgdiff(card,trainCard))
    res.append(r[:])
