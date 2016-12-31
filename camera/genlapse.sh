#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin
cd /home/pi/rpi/camera/pics
ls *.jpg > stills.txt
DATE=$(date +"%Y-%m-%d")
echo "========== Start mencoder =========="
mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=8000000 -vf scale=1920:1080 -o $DATE.avi -mf type=jpeg:fps=24 mf://@stills.txt
echo "========== mencoder finished, start MP4Box =========="
MP4Box -add $DATE.avi ../videos/$DATE.mp4
echo "========== MP4Box finishes =========="
rm $DATE.avi
rm *.jpg
cd ..
