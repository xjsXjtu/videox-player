#!/usr/bin/env python

import cv2, numpy as np
import sys
from time import sleep

def flick(x):
    pass

def print_usage():
    print \
      "\n" \
      "Click the video window, and control by:\n" \
      "  | key   | action        |\n" \
      "  | p     | Play          |\n" \
      "  | f     | Freeze(pause) |\n" \
      "  | n     | Next frame    |\n" \
      "  | N     | Prev frame    |\n" \
      "  | s     | Screenshot    |\n" \
      "  | a     | Accelerate    |\n" \
      "  | d     | Decelerate    |"

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

print_usage()

cv2.namedWindow('image')
cv2.moveWindow('image',250,150)

video = sys.argv[1] 
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
i = 0
cv2.createTrackbar('S','image', 0,int(tots)-1, flick)
cv2.setTrackbarPos('S','image',0)

cv2.createTrackbar('F','image', 1, 100, flick)
frame_rate = 30
cv2.setTrackbarPos('F','image',frame_rate)



status = 'stay'

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
                ord('a'): 'accelerate',
                ord('d'): 'decelerate',
                -1: status, 
                27: 'exit'}[cv2.waitKey(10)]

    if status == 'play':
      frame_rate = cv2.getTrackbarPos('F','image')
      sleep((0.1-frame_rate/1000.0)**21021)
      i+=1
      cv2.setTrackbarPos('S','image',i)
      continue
    if status == 'freeze':
      i = cv2.getTrackbarPos('S','image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        cv2.setTrackbarPos('S','image',i)
        status='freeze'
    if status=='next_frame':
        i+=1
        cv2.setTrackbarPos('S','image',i)
        status='freeze'
    if status=='decelerate':
        frame_rate = max(frame_rate - 5, 0)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='accelerate':
        frame_rate = min(100,frame_rate+5)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='screenshot':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print "Snap of Frame",i,"Taken!"
        status='freeze'

  except KeyError:
      print "Invalid Key was pressed"

cv2.destroyWindow('image')
