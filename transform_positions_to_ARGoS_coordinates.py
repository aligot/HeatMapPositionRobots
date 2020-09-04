import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--positions", help = "path to the positions")
args = vars(ap.parse_args())

data = pd.read_csv(args["positions"], header = None)

initial_positions = data.loc[(data[0] == 0)]
initial_positions.columns= ["Frame", "X", "Y", "Radius"]

nbPositions = initial_positions["Frame"].count()

x = initial_positions.X.tolist()
y = initial_positions.Y.tolist()
radius = initial_positions.Radius.tolist()

print(len(x))


# Removing extra points based on distance between detected points
toBeRemoved = []
for i in range(nbPositions-1):
	for j in range(i+1,nbPositions):
		a = np.array((x[i], y[i]))
		b = np.array((x[j], y[j]))
		dist = np.linalg.norm(a-b)
		if (dist < 30):
			if (radius[i] >= radius[j]):
				toBeRemoved.append(j)
			else:
				toBeRemoved.append(i)

for index in sorted(toBeRemoved, reverse=True):
	del x[index]
	del y[index]


print(len(x))

#Transforming into coordinates with (0,0) in the middle
widthOriginalFrame = 1200
heightOriginalFrame = 1190

pixel_to_meter_factor = 2.5/1200

new_x = [pixel_to_meter_factor*(i - widthOriginalFrame/2) for i in x]
new_y = [pixel_to_meter_factor*(i - widthOriginalFrame/2) for i in y]

output = "<e-puck id=\"epuck_{}\"> \n <body orientation=\"0,0,0\" position=\"{},{},0\" /> \n <controller config=\"nn_rm_1dot1\" /> \n</e-puck>"

for i in range(len(new_x)):
	print(output.format(i, -new_x[i], new_y[i]))
