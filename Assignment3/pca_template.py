
# coding: utf-8
import numpy as np
from numpy import *
from scipy.linalg import eigh
from numpy.linalg import eig
from matplotlib import pyplot as plt
import sys


def loadDataSet(fileName = 'iris_with_cluster.csv'):
    dataMat=[]
    labelMat=[]
    fr = open(fileName)
    for line in fr.readlines():
        lineArray=line.strip().split(',')
        records = []
        for attr in lineArray[:-1]:
            records.append(float(attr))
        dataMat.append(records)
        labelMat.append(int(lineArray[-1]))
    dataMat = array(dataMat)
    
    labelMat = array(labelMat)
    
    
    return dataMat,labelMat

def pca(dataMat, PC_num=2):
    '''
    Input:
        dataMat: obtained from the loadDataSet function, each row represents an observation
                 and each column represents an attribute
        PC_num:  The number of desired dimensions after applyting PCA. In this project keep it to 2.
    Output:
        lowDDataMat: the 2-d data after PCA transformation
    '''
    mean = dataMat.mean(axis=0, keepdims=True)
    adjustedData = dataMat - dataMat.mean(axis=0, keepdims=True)
    covMat = np.cov(adjustedData, rowvar=False)

    w, v = eig(covMat)
    val, vect = eigh(covMat, subset_by_index=[len(w)-2, len(w)-1])
    print("EIGVAL: ", val, "EIGVECT: ", vect)
    lowDDataMat = np.matmul(adjustedData, vect)
    return array(lowDDataMat)


def plot(lowDDataMat, labelMat, figname):
    '''
    Input:
        lowDDataMat: the 2-d data after PCA transformation obtained from pca function
        labelMat: the corresponding label of each observation obtained from loadData
    '''
    plt.scatter(lowDDataMat[:,0], lowDDataMat[:,1], c = labelMat)
    plt.title(figname)
    plt.show()

    


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = 'iris_with_cluster.csv'
    figname = filename
    figname = figname.replace('csv','jpg')
    dataMat, labelMat = loadDataSet(filename)
    lowDDataMat = pca(dataMat)
    
    plot(lowDDataMat, labelMat, figname)
    

