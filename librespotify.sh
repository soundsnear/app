#!/bin/bash
#here we send standard output to a file
./librespot -b 320 -c /tmp --name 'just me here' --backend alsa --device plughw:0 >/tmp/infoli 2>&1
#we read the file and extract only track title
cut -d: -f5 /tmp/infoli | cut -d -f2 | tail -1