# videos-player

Refering the use of OpenCV in the original repo,
I greatly refactored the code, make it:
 * More clear in the software structure
 * Easier to add new file format

## Motivation

Damn!

I just want to view YUV file on Mac.

I googled, and the options on Mac are:
 * The [PYUV: raw video sequence player](http://dsplab.diei.unipg.it/software/pyuv_raw_video_sequence_player): I tried but it frozen after playing only one frame.
 * [MPV](https://github.com/mpv-player/mpv):complicated, tut YUV in not supported.
 * [YUView](https://github.com/IENT/YUView): cross-platform and wonderful analytic toolset. But crash after I tried the prebuilt binary.

I suppose it’s simple by opencv+python.

Let’s make it by own hand. 

## Features

Currently only supports the following formats:
 * encoded video file in containers supported by opencv, such as mp4.
 * YUV420

Please let me know if you want supporting other formats.

videos-player is controlled by keyboard:

| key | action |
| -     | -|
| p     | Play |
| f     | Freeze(pause) |
| n     | Next frame|
| N     | Last frame|
| s     | Screenshot |
