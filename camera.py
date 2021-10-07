import numpy as np
import cv2
import os
import time


def main():
    cap = cv2.VideoCapture(-1)
    cap.set(3,640)
    cap.set(4,480)
    while(cap.isOpened()):
        #------------------------------------[1] load img and flip
        _,src = cap.read()
        src = cv2.flip(src,-1)
        cv2.imshow('src',src)
        #------------------------------------[2] crop, color, blur, resize
        height,_,_  = src.shape
        out = src[int(height/2): , : , : ]
        out = cv2.cvtColor(out,cv2.BGR2YUV)
        out = cv2.GaussianBlur(out,(3,3),0)
        out = cv2.resize(out,dsize = (200,66))
        cv2.imshow("out",out)
        #------------------------------------[3] save

        










        if cv2.waitKey(1)==ord('q'):
            break
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
