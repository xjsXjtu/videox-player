#!/usr/bin/env python

import cv2, numpy as np
import sys
import time
import re
import os

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
        else:
            assert(False)

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
        self._capture.set(cv2.CAP_PROP_POS_FRAMES, pos)

class DecoderYuv420(object):
    def __init__(self, filename):
        self._file       = open(filename, 'rb')
        self._file_bytes = os.stat(filename).st_size
        
        words = re.split('_|-|x|\.', filename)
        if len(words) < 3:
            print "Filename must be [xxxx_]with_height.yuv"
            assert(False)
        self._with      = int(words[-3])
        self._height    = int(words[-2])
        self._im_bytes  = self._with * self._height * 3 / 2
        self._y_bytes   = self._with * self._height
        self._frames    = self._file_bytes / self._im_bytes
        self._framerate = 30
        
        self._cur_pos_in_frame = 0

    def GetTotalFrames(self):
        return self._frames
    
    def GetFramerate(self):
        return self._framerate
    
    def GetCurFrame(self):
        cur_pos_byte = self._im_bytes * self._cur_pos_in_frame
        if cur_pos_byte + self._im_bytes > self._file_bytes:
            cur_pos_byte = 0
        self._file.seek(cur_pos_byte)
        y = np.fromfile(self._file, np.uint8, self._y_bytes).reshape(-1, self._with)
        u = np.fromfile(self._file, np.uint8, self._y_bytes / 4).reshape(-1, self._with / 2)
        v = np.fromfile(self._file, np.uint8, self._y_bytes / 4).reshape(-1, self._with / 2)
        #bgr = (np.random.rand(50, 50, 3) * 255).astype(np.uint8)
        return (True, self._ConvertYUV420toBGR(y, u, v))
            
    def SetPosInFrame(self, pos):
        self._cur_pos_in_frame = pos

    # Ref: https://en.wikipedia.org/wiki/YUV#Y.E2.80.B2UV420p_.28and_Y.E2.80.B2V12_or_YV12.29_to_RGB888_conversion    
    def _ConvertYUV420toBGR(self, y, u, v):
        u = u.repeat(2, axis=0).repeat(2, axis=1)
        v = v.repeat(2, axis=0).repeat(2, axis=1)
        # ITU-R standard
        y  = y.reshape((y.shape[0], y.shape[1], 1)).astype(np.int)
        u  = u.reshape((u.shape[0], u.shape[1], 1)).astype(np.int) - 128
        v  = v.reshape((v.shape[0], v.shape[1], 1)).astype(np.int) - 128
        r = (1 * y + 0     * u + 1.402 * v)
        g = (1 * y - 0.344 * u - 0.714 * v)
        b = (1 * y + 1.772 * u + 0     * v)
        return np.concatenate((b, g, r), axis=2).clip(0, 255).astype(np.uint8)
        
        
