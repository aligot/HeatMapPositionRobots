import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", help = "path to the file containing the coordinates")
# args = vars(ap.parse_args())

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

mypath = "/home/aligot/Desktop/Arena/HeatmapPositionRobots/ExtendedPoints/"
all_df = getListOfFiles(mypath)

for f in all_df:
    full_name = os.path.splitext(os.path.basename(f))[0]
    short_name = full_name.split("_seed")[0]

    print(short_name)

    data = pd.read_csv(f, skiprows=0)

    x = data.X.tolist()
    y = data.Y.tolist()

    plt.figure(figsize=cm2inch(15.5,15.2))
    plt.hist2d(x,y, bins=[np.arange(0,1200,1),np.arange(0,1190,1)],cmin=1)
    plt.gca().set_ylim([0,1190])
    plt.gca().set_xlim([0,1200])
    plt.gca().invert_yaxis()
    plt.axis('off')
    plt.tight_layout()

    outputname = "/home/aligot/Desktop/Arena/HeatmapPositionRobots/Plots/" + short_name + ".png"
    plt.savefig(outputname, format='png', bbox_inches='tight', transparent=True, dpi=200)
    plt.close()
