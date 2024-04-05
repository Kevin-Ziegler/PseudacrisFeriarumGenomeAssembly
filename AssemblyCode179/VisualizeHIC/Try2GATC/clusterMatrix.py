import numpy as np
matrixFile = "matrixHIC_GATC_2.txt"

input = np.loadtxt(matrixFile, dtype='i', delimiter=' ')


from sklearn.cluster import SpectralClustering
from sklearn import metrics
np.random.seed(0)

adj_mat = [[3,2,2,0,0,0,0,0,0],
           [2,3,2,0,0,0,0,0,0],
           [2,2,3,1,0,0,0,0,0],
           [0,0,1,3,3,3,0,0,0],
           [0,0,0,3,3,3,0,0,0],
           [0,0,0,3,3,3,1,0,0],
           [0,0,0,0,0,1,3,1,1],
           [0,0,0,0,0,0,1,3,1],
           [0,0,0,0,0,0,1,1,3]]

adj_mat = np.array(adj_mat)

adj_mat = input

sc = SpectralClustering(22, affinity='precomputed', n_init=100)
sc.fit(adj_mat)

print('spectral clustering')
print(sc.labels_)

for i in range(0, len(sc.labels_)):
	print(sc.labels_[i])

#from sklearn.cluster import DBSCAN

#clustering = DBSCAN(metric='precomputed')
#clustering.fit(distance_matrix)



