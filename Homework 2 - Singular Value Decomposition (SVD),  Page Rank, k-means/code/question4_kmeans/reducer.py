#!/usr/bin/python

import sys
import numpy as np

def compute_new_centroids():
    cost = 0
    centroids = dict()
    for line in sys.stdin:

        line = line.strip().split(",")

        # Ignoring cost from previous iteration
        if len(line) == 1:
            continue

        cluster_num = int(line[0])
        point = np.array(map(float, line[1].strip().split()))
        cost += float(line[2])

        if cluster_num not in centroids:
            centroids[cluster_num] = (point, 1)
        else:
            centroids[cluster_num] = (centroids[cluster_num][0] + point, centroids[cluster_num][1] + 1)

    for _, value in centroids.items():
        new_cluster = value[0] / value[1]
        print(' '.join(map(str, new_cluster)))
    print(cost)

if __name__ == "__main__":
    compute_new_centroids()
