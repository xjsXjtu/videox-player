#!/usr/bin/env python

import cv2, numpy as np
import sys
from time import sleep

PROGRESS_BAR = "progress_bar"
SPEED_BAR    = "speed_bar"

frame_rate = 30

def OnProgressBarChanged(x):
    pass

def OnSpeedBarChanged(x):
    frame_rate = x

def print_usage():
    print \
      "\n" \
      "Click the video window, and control by:\n" \
      "  | key   | action        |\n" \
      "  | p     | Play          |\n" \
      "  | f     | Freeze(pause) |\n" \
      "  | n     | Next frame    |\n" \
      "  | N     | Prev frame    |\n" \
      "  | s     | Screenshot    |\n"

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


print_usage()

cv2.namedWindow('image')
cv2.moveWindow('image',250,150)

video = sys.argv[1] 
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
i = 0
cv2.createTrackbar(PROGRESS_BAR,'image', 0,int(tots)-1, OnProgressBarChanged)
cv2.setTrackbarPos(PROGRESS_BAR,'image',0)

cv2.createTrackbar(SPEED_BAR,'image', 1, 100, OnSpeedBarChanged)
cv2.setTrackbarPos(SPEED_BAR,'image',frame_rate)

status = 'freeze'

while True:
  try:
    if i==tots-1:
      i=0
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    r = 750.0 / im.shape[1]
    dim = (750, int(im.shape[0] * r))
    im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow('image', im)
    status = {  ord('f'): 'freeze',
                ord('p'): 'play',
                ord('N'): 'prev_frame',
                ord('n'): 'next_frame',
                ord('s'): 'screenshot',
                -1: status, 
                27: 'exit'}[cv2.waitKey(10)]

    if status == 'play':
      frame_rate = cv2.getTrackbarPos('F','image')
      sleep((0.1-frame_rate/1000.0)**21021)
      i+=1
      cv2.setTrackbarPos(PROGRESS_BAR,'image',i)
      continue
    if status == 'freeze':
      i = cv2.getTrackbarPos(PROGRESS_BAR,'image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        cv2.setTrackbarPos(PROGRESS_BAR,'image',i)
        status='freeze'
    if status=='next_frame':
        i+=1
        cv2.setTrackbarPos(PROGRESS_BAR,'image',i)
        status='freeze'
    if status=='screenshot':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print "Snap of Frame",i,"Taken!"
        status='freeze'

  except KeyError:
      print "Invalid Key was pressed"

cv2.destroyWindow('image')
