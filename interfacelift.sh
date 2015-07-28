#!/bin/bash

IMGPATH=`python interfacelift.py`

osascript -e "tell application \"Finder\"
set desktop picture to POSIX file \"`pwd`/$IMGPATH\"
end tell"
