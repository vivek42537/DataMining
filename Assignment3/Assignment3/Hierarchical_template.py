
# coding: utf-8

import sys
from matplotlib import pyplot as plt
import numpy as np
from numpy import *
import copy
import csv
import math
from scipy.spatial import distance

def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        fltLine = list(map(float,curLine)) #map all elements to float()
        dataMat.append(fltLine)
    return np.array(dataMat)


def merge_cluster(distance_matrix, cluster_candidate, T):
    ''' Merge two closest clusters according to min distances
    1. Find the smallest entry in the distance matrix—suppose the entry 
        is i-th row and j-th column
    2. Merge the clusters that correspond to the i-th row and j-th column 
        of the distance matrix as a new cluster with index T

    Parameters:
    ------------
    distance_matrix : 2-D array
        distance matrix
    cluster_candidate : dictionary
        key is the cluster id, value is point ids in the cluster
    T: int
        current cluster index

    Returns:
    ------------
    cluster_candidate: dictionary
        upadted cluster dictionary after merging two clusters
        key is the cluster id, value is point ids in the cluster
    merge_list : list of tuples
        records the two old clusters' id and points that have just been merged.
        [(cluster_one_id, point_ids_in_cluster_one), 
         (cluster_two_id, point_ids_in_cluster_two)]
    '''

    # TODO
    merge_list = []

    minValue = np.amin(distance_matrix)
    index = np.where(distance_matrix == np.amin(distance_matrix))
    i = index[0]
    j = index[1]
    # print("matrix: ", distance_matrix)
    if len(i) > 1:
        a = i[0]
        b = i[1]
    else :
        a = i[0]
        b = j[0]
    # print("a: ", a, "b: ", b)
    # print("min: ", minValue)
    # print("cluster Before: ", cluster_candidate)
    # print("mergeList: ", merge_list)
    for k,v in cluster_candidate.items() :
        for x in v:
            if x == a:
                # print("Key: ", k, "Val: ", v)
                pop1 = k
                val1 = v

    for k,v in cluster_candidate.items() :
        for x in v:
            if x == b:
                # print("Key: ", k, "Val: ", v)
                pop2 = k
                val2 = v

    merge_list.append(tuple(((pop1, val1))))
    merge_list.append(tuple((pop2, val2)))

    if pop1 != pop2:
        cluster_candidate.pop(pop1)
        cluster_candidate.pop(pop2)
        temp = []
        for oney in val1:
            temp.append(oney)
        for twoy in val2:
            temp.append(twoy)

        cluster_candidate[T] = temp

    # print("cluster After: ", cluster_candidate)
    return cluster_candidate, merge_list


def update_distance(distance_matrix, cluster_candidate, merge_list):
    ''' Update the distantce matrix
    
    Parameters:
    ------------
    distance_matrix : 2-D array
        distance matrix
    cluster_candidate : dictionary
        key is the updated cluster id, value is a list of point ids in the cluster
    merge_list : list of tuples
        records the two old clusters' id and points that have just been merged.
        [(cluster_one_id, point_ids_in_cluster_one), 
         (cluster_two_id, point_ids_in_cluster_two)]

    Returns:
    ------------
    distance_matrix: 2-D array
        updated distance matrix       
    '''
    
    # TODO
    # print("distanceMatrix: ", distance_matrix)
    x = merge_list[0][1]
    y = merge_list[1][1]
    # i = x[0]
    # j = y[0]
    for i in x:
        for j in y:
            # print("i: ", i, "j: ", j)
            distance_matrix[i][j] = 100000
            distance_matrix[j][i] = 100000

    return distance_matrix  

    

def agglomerative_with_min(data, cluster_number):
    """
    agglomerative clustering algorithm with min link

    Parameters:
    ------------
    data : 2-D array
        each row represents an observation and 
        each column represents an attribute

    cluster_number : int
        number of clusters

    Returns:
    ------------
    clusterAssment: list
        assigned cluster id for each data point
    """
    cluster_candidate = {}
    N = len(data)
    # initialize cluster, each sample is a single cluster at the beginning
    for i in range(N):
        cluster_candidate[i+1] = [i]  #key: cluser id; value: point ids in the cluster

    # initialize distance matrix
    distance_matrix = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if j == i: # or j<=i
                distance_matrix[i,j] = 100000
            else:
                distance_matrix[i,j] = np.sqrt(np.sum((data[i]-data[j])**2))
    
    # hiearchical clustering loop
    T = N + 1 #cluster index
    for i in range(N-cluster_number):
        cluster_candidate, merge_list = merge_cluster(distance_matrix, cluster_candidate, T)
        distance_matrix   = update_distance(distance_matrix, cluster_candidate, merge_list )
        print('%d-th merging: %d, %d, %d'% (i, merge_list[0][0], merge_list[1][0], T))
        T += 1
        # print(cluster_candidate)


    # assign new cluster id to each data point 
    clusterAssment = [-1] * N
    for cluster_index, cluster in enumerate(cluster_candidate.values()):
        for c in cluster:
            clusterAssment[c] = cluster_index
    # print (clusterAssment)
    return clusterAssment


def saveData(save_filename, data, clusterAssment):
    clusterAssment = np.array(clusterAssment, dtype = object)[:,None]
    data_cluster = np.concatenate((data, clusterAssment), 1)
    data_cluster = data_cluster.tolist()

    with open(save_filename, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(data_cluster)
    f.close()



if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_filename = sys.argv[1]
        cluster_number = int(sys.argv[2])
    else:
        print("poo")
        data_filename = 'Example.csv'
        cluster_number = 1

    save_filename = data_filename.replace('.csv', '_hc_cluster.csv')

    data = loadDataSet(data_filename)

    clusterAssment = agglomerative_with_min(data, cluster_number)

    saveData(save_filename, data, clusterAssment)
