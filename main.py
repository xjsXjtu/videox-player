#!/usr/bin/env python

import cv2, numpy as np
import sys
import time
from player import Player, FileFormat, PlayerState, PlayerCmd

def PrintUsage():
    print \
      "\n" \
      "Click the video window, and control by:\n" \
      "  | key   | action        |\n" \
      "  | p     | Play          |\n" \
      "  | f     | Freeze(pause) |\n" \
      "  | n     | Next frame    |\n" \
      "  | N     | Prev frame    |\n" \
      "  | s     | Screenshot    |\n"

def main():
    PrintUsage()
    player = Player(sys.argv[1], FileFormat.AUTO_DETECT)
    player.Start()

    while True:
        try:
            cmd = 'none'
            cmd = {ord('f'): 'freeze',
                   ord('p'): 'play',
                   ord('N'): 'prev_frame',
                   ord('n'): 'next_frame',
                   ord('s'): 'screenshot',
                   -1      : cmd, 
                   27      : 'exit'}[cv2.waitKey(10)]
            if cmd == 'play':
                player.Play()
            if cmd == 'freeze':
                player.Pause()
            if cmd == 'exit':
                player.Stop()
                break
            if cmd == 'prev_frame':
                player.SeekTo(player.GetCurPos() - 1)
                player.Pause()               
            if cmd == 'next_frame':
                player.SeekTo(player.GetCurPos() + 1)
                player.Pause()
            if cmd == 'screenshot':
                player.SaveCurFrame()
                player.Pause()           
        except KeyError:
            print "Invalid Key was pressed"
        except (KeyboardInterrupt):
            print "KeyboardInterrupt in main()"
            player.Stop()
            sys.exit()

if __name__ == "__main__":
    main()

