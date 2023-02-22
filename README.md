# HeatMapPositionRobots

Series of scripts that collects the position of e-puck robots from videos and create heatmaps.


In simulation videos, robots are depicted with bright green, making it easy to detect.
color_detector_video.py detects the robots using their colors.

In reality videos, the robots have white tags on top of them, which can blend in with white foor.
Plus, the quality of the videos is poor, making color_detector_video.py unusable. Instead,
shape_detector_video.py dectects the robots using their contour. 

These scripts were used to generate the following figure:
https://www.nature.com/articles/s41467-021-24642-3/figures/6
