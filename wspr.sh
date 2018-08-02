#!/bin/bash

pacmd load-module module-null-sink sink_name=Virtual1
pacmd update-sink-proplist Virtual1 device.description=Virtual1
pacmd load-module module-loopback sink=Virtual1
pacmd load-module module-null-sink sink_name=Virtual2
pacmd update-sink-proplist Virtual2 device.description=Virtual2
pacmd load-module module-loopback sink=Virtual2
pacmd load-module module-null-sink sink_name=Virtual3
pacmd update-sink-proplist Virtual3 device.description=Virtual3
pacmd load-module module-loopback sink=Virtual3

wsjtx --rig-name=WSPR20m&
wsjtx --rig-name=WSPR40m&
wsjtx --rig-name=WSPR30m&

python ~/workspace/cvanbogaert-public/gr-learning/top_block.py&

