import cv2
import numpy as np
from setgameLib import *
trainSet = ['train/'+str(i)+'.jpg' for i in range(9)]

for i, card in enumerate(train(trainSet)):
    savefile = 'images/res'+str(i)+'.jpg'
    cv2.imwrite(savefile,card)
