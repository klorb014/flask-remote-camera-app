#!/usr/bin/env bash
rmmod uvcvideo
modprobe uvcvideo nodrop=1 timeout=5000
source ~/python/bin/activate
python ~/python/camera/app.py