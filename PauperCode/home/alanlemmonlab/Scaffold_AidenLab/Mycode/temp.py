import pickle
#from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy as np

dictionaryFile = "CHI_purgedups_Trimmed_Connections_Locations.pickle"
#contigsFile = "RepurgedContigLengths_3_29_2024.txt"
#chicDict = {}
#fileOut = "MyChicagoConnections.txt"

#fout = open(fileOut, 'w')

minAreaRatio = 0.1
maxLength = 100
distanceAllowed = 40000



with open(dictionaryFile, "rb") as file:
        chiDict = pickle.load(file)



#string = "tig00058886_1_tig00002749_1"

string = "tig00070108_1_tig00002870_1"

print(chiDict[string])

import matplotlib.pyplot as plt

xy = chiDict[string]

x = []
y = []
for item in xy:
	x.append(int(item[0]))
	y.append(int(item[1]))

plt.plot(x, y, 'bo')
plt.show()
