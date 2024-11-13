#!/bin/bash
gst-launch-1.0 -v v4l2src device=/dev/video0 num-buffers=-1 ! video/x-raw, width=640, height=480 framerate=30/1 ! videoconvert ! jpegenc ! rtpjpegpay ! udpsink host=192.168.8.100 port=5200