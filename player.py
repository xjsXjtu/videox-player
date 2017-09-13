#!/usr/bin/env python

import cv2, numpy as np
import sys
import time
import threading

from decoder import FileFormat, DecoderFactory


class PlayerState(object):
    PLAYING = 0
    PAUSED  = 1
    STOPPED = 2

class PlayerCmd(object):
    PLAY       = 0
    FREEZE     = 1
    NEXT_FRAME = 2
    PREV_FRAME = 3
    SCREENSHOT = 4

class Player(object):
    def __init__(self, filename, fileformat):
        self._filename  = filename
        self._fileformat    = fileformat
        self._framerate = -1
        self._cur_pos   = 0
        self._state     = PlayerState.PAUSED
        self._lock      = threading.RLock()

        self._win          = "player"
        self._PROGRESS_BAR = "progress:"
        self._SPEED_BAR    = "speed   :"
        assert(self._Init())

    def _Init(self):
        cv2.namedWindow(self._win)
        cv2.moveWindow(self._win, 250, 150)

        self._decoder      = DecoderFactory().Create(
                                  self._filename, self._fileformat)
        self._total_frames = self._decoder.GetTotalFrames()
        self._framerate    = self._decoder.GetFramerate()

        cv2.createTrackbar(self._PROGRESS_BAR, self._win,
                           0, int(self._total_frames) - 1,
                           self._OnProgressBarChanged)
        cv2.setTrackbarPos(self._PROGRESS_BAR, self._win,
                           self._cur_pos)
        cv2.createTrackbar(self._SPEED_BAR, self._win,
                           1, 10 * int(self._framerate + 0.5),
                           self._OnSpeedBarChanged)
        cv2.setTrackbarPos(self._SPEED_BAR, self._win,
                           int(self._framerate + 0.5))
        return True
        
    def __del__(self):
        cv2.destroyWindow(self._window)

    def _OnProgressBarChanged(self, x):
        pass

    def _OnSpeedBarChanged(self, x):
        with self._lock:
            self._framerate = x
        
    def Start(self):
        with self._lock:
            self._thread = threading.Thread(
                target = self._ThreadProc,
                args =  ())
            self._thread.start()
            self.Play()

    def Stop(self):
        print 'stop'
        with self._lock:
            self._state = PlayerState.STOPPED
            self._thread.join()

    def Play(self):
        print 'play'
        with self._lock:
            self._state = PlayerState.PLAYING

    def Pause(self):
        print 'pause'
        with self._lock:
            self._state = PlayerState.PAUSED

    def SetFramerate(self, framerate):
        with self._lock:
            self._framerate = framerate
   
    def GetCurPos(self):
        with self._lock:
            return self._cur_pos
 
    def SeekTo(self, pos_in_frame):
        print 'seek'
        with self._lock:
            self._cur_pos   = pos_in_frame
            self._ShowCurFrame()

    def SaveCurFrame(self):
        with self._lock:
            ret, im = self._decoder.GetCurFrame()
            filename = "./" + "Frame_" + str(self.GetCurPos())+".jpg"
            cv2.imwrite(filename, im)
            print "Saved Frame: " + filename

    def _ThreadProc(self):
        while self._state in [PlayerState.PLAYING, PlayerState.PAUSED]:
            with self._lock:
                self._OneLoopLocked()
            time.sleep(1.0 / self._framerate)

    def _OneLoopLocked(self):
        try:
            if self._state == PlayerState.PLAYING:
                if self._cur_pos == self._total_frames - 1:
                    self._cur_pos = 0
                self._ShowCurFrame()
                self._cur_pos += 1
            elif self._state == PlayerState.PAUSED:
                pass
            else:
                assert(False)
        except:
            pass
        
    def _ShowCurFrame(self):
        # TODO: use an Decoder interface
        self._decoder.SetPosInFrame(self._cur_pos)
        ret, im = self._decoder.GetCurFrame()
        r   = 750.0 / im.shape[1]
        dim = (750, int(im.shape[0] * r))
        im  = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow(self._win, im)
        cv2.setTrackbarPos(self._PROGRESS_BAR, self._win,
                           self._cur_pos)
                
