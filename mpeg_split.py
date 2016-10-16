#!/usr/bin/python
# code to read a csv file of detected movements,
# calculate windows of movement and cut original video up into those windows

import csv
import os
import sys
import re
windowsize = 30  # size of initial movement window in seconds
windowextension = 30  # size of extention to window in seconds
hardlimit = 300  # hard limit on video length
movethreshold = 3  # movement threshold
f = sys.argv[1]
with open(f + ".csv", 'r') as csvfile:
    csreader = csv.reader(csvfile, delimiter=',')
    filestart = True
    for row in csreader:
        if float(row[3]) > movethreshold:
            if (filestart is True):
                starttime = int(row[1]) * 60 + int(row[2])
                # if motion near start of video, make snippet start at start
                if (starttime < 3):
                    starttime = 0
                else:
                    starttime = starttime - 2  # add 2 seconds before motion
                    filestart = False
                    endtime = starttime + windowsize
            else:
                nexttime = int(row[1]) * 60 + int(row[2])
                if (nexttime < endtime) and (nexttime > endtime - windowextension):
                    endtime = nexttime + windowextension
                elif (nexttime > endtime):
                    # run ffmpeg here
                    if (endtime - starttime) > hardlimit:
                        endtime = starttime + hardlimit
                        os.system(
                            "ffmpeg -i " + f + ".mp4 -ss " +
                            str(starttime) + " -to " + str(endtime) +
                            " -async 1 " + f + "_" + str(starttime) +
                            "-" + str(endtime) + ".mp4")
                        os.system(
                            "ffmpeg -i " + f + ".mp4 -ss " +
                            str(starttime) + " -vframes 1 " + f + "_" +
                            str(starttime) + "-" + str(endtime) + ".png")
                        starttime = starttime + hardlimit - 2
                        endtime = starttime + windowsize
                    else:
                        os.system(
                            "ffmpeg -i " + f + ".mp4 -ss " +
                            str(starttime) + " -to " + str(endtime) +
                            " -async 1 " + f + "_" + str(starttime) +
                            "-" + str(endtime) + ".mp4")
                        os.system(
                            "ffmpeg -i " + f + ".mp4 -ss " +
                            str(starttime) + " -vframes 1 " + f + "_" +
                            str(starttime) + "-" + str(endtime) + ".png")
                        starttime = nexttime - 2
                        endtime = starttime + windowsize
    # run ffmpeg over last segment
    os.system(
        "ffmpeg -i " + f + ".mp4 -ss " + str(starttime) + " -to " +
        str(endtime) + " -async 1 " + f + "_" + str(starttime) +
        "-" + str(endtime) + ".mp4")
    os.system(
        "ffmpeg -i " + f + ".mp4 -ss " +
        str(starttime) + " -vframes 1 " + f + "_" + str(starttime) +
        "-" + str(endtime) + ".png")
