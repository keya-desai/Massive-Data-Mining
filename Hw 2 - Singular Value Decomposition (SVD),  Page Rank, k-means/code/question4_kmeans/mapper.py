#!/usr/bin/env python

import sys
from math import sqrt
import numpy as np
# import pdb

# def distance(point, centroid):

#         # l = [pow(float((p_i)) - float((c_i)),2) for p_i,c_i in zip(point,centroid)] 
#         return sqrt(sum(l))

def get_centroids(filepath):
        centroids = []
        file = open(filepath, "rb")
        for i, line in enumerate(file.readlines()):
                if i == 10:
                    continue
                centroid = np.array(list((map(float, line.strip().split()))))
                centroids.append(centroid)
                file.close()

        return np.array(centroids)

def clusters(centroids):

        for line in sys.stdin:
                # print("line :", line)
                point = np.array(list(map(float,line.strip().split())))
                # print("point = ", point)
                # print("centroids = ", centroids.shape)
                # pdb.set_trace()
                euclidian_distances = np.sqrt(((centroids - point)**2).sum(axis = 1))
                min_dist, cluster_num = np.min(euclidian_distances), np.argmin(euclidian_distances)
                print("%s,%s,%s" % (cluster_num, line.strip(), str(min_dist**2)))


if __name__ == "__main__":
        centroids = get_centroids('./c1/centroids.txt')
        clusters(centroids)

        




