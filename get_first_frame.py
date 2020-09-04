import cv2
import argparse
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import time


ts = time.gmtime()
ts = time.strftime("%Y%m%d%H%M%S", ts)
# 2020-08-24 09:18:01


# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help = "path to the video")
# args = vars(ap.parse_args())
# load the video
#cap = cv2.VideoCapture(args["video"])
mypath = "/home/aligot/Desktop/Arena/HeatmapPositionRobots/Videos/median_runs/"

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

all_videos = getListOfFiles(mypath)

for i, v in enumerate(all_videos):
    f = v.split('/')
    name = f[len(f)-2] + "_" + f[len(f)-1]
    output_file_name = os.path.splitext(name)[0]
    LastFrameName = "FirstFrames/" + output_file_name + ".jpg"


    print(output_file_name)

    cap = cv2.VideoCapture(v)

    count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(count)


    frame_cnt = 0
    # Loop untill the end of the video
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if (frame_cnt == 0):
            frame = frame[30:1230, 150:1350]
            cv2.imwrite(LastFrameName, frame)
            print("Frame saved")
            cap.release()

        frame_cnt += 1

    #cv2.imshow('Thresh', frame)


# release the video capture object
