#!/usr/bin/env python

import cv2, numpy as np
import sys
import time

class FileFormat(object):
    YUV420 = 0
    AUTO_DETECT = 1

class DecoderFactory(object):
    def __init__(self):
        pass
    def Create(self, filename, fileformat):
        if fileformat == FileFormat.AUTO_DETECT:
            return DecoderOpencv(filename)
        elif fileformat == FileFormat.YUV420:
            return DecoderYuv420(filename)

class DecoderOpencv(object):
    def __init__(self, filename):
        self._capture = cv2.VideoCapture(filename)

    def GetTotalFrames(self):
        return self._capture.get(cv2.CAP_PROP_FRAME_COUNT)
    def GetFramerate(self):
        return self._capture.get(cv2.CAP_PROP_FPS)
    def GetCurFrame(self):
        return self._capture.read()
    def SetPosInFrame(self, pos):
        return self._capture.set(cv2.CAP_PROP_POS_FRAMES, pos)

class DecoderYuv420(object):
    def __init__(self, filename):
        pass
