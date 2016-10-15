#!/usr/bin/python
import csv
import os
import sys
import re
windowsize = 120
windowextension = 30
f = sys.argv[1]
with open(f + ".csv", 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    filestart = True
    for row in spamreader:
        if (filestart is True):
            starttime = row[1] * 60 + row[2]
            if (starttime < 2):
                starttime = 0
            else:
                starttime = starttime - 2
            filestart = False
            endtime = starttime + windowsize
        else:
            nexttime = row[1] * 60 + row[2]
            if (nexttime < endtime):
                endtime = nexttime + windowextension
            else:
                # run ffmpeg here
                os.system(
                    "ffmpeg -i " + f + ".mp4 -ss " + starttime + " -to " +
                    endtime + " -async 1 " + f + "_" + starttime + "-" +
                    endtime + ".mp4")
                starttime = nexttime
                endtime = starttime + windowsize
