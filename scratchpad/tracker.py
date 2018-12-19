#!/usr/bin/env python3

import cv2
import numpy as np


cap = cv2.VideoCapture(2)

while (cap.isOpened()):
    ret, frame = cap.read()
    bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = bw[10:500,250:290]
    h, w = img.shape
    for i in range(0, h):
        if np.average(img[i] < 50):
            for j in range(0, w):
              frame[i][j][0] = 0
              frame[i][j][1] = 0
              frame[i][j][2] = 255
            break
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
