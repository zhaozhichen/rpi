#!/bin/bash
 DATE=$(date +"%Y-%m-%d_%H%M")
 raspistill -o /home/pi/rpi/camera/pics/$DATE.jpg
