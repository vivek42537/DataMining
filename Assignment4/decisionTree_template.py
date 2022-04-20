
import treeplot
from collections import Counter

def loadDataSet(filepath):
    '''
    Returns
    -----------------
    data: 2-D list
        each row is the feature and label of one instance
    featNames: 1-D list
        feature names
    '''
    data=[]
    featNames = None
    fr = open(filepath)
    for (i,line) in enumerate(fr.readlines()):
        array=line.strip().split(',')
        if i == 0:
            featNames = array[:-1]
        else:
            data.append(array)
    return data, featNames


def splitData(dataSet, axis, value):
    '''
    Split the dataset based on the given axis and feature value

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label
    axis: int 
        index of which feature to split on
    value: string
        the feature value to split on

    Returns
    ------------------
    subset: 2-D list 
        the subset of data by selecting the instances that have the given feature value
        and removing the given feature columns
    '''
    subset = []
    for instance in dataSet:
        if instance[axis] == value:    # if contains the given feature value
            reducedVec = instance[:axis] + instance[axis+1:] # remove the given axis
            subset.append(reducedVec)
    return subset

def gini(data):

    labelList = []
    for x in data:
        feat = x[0]
        labelList.append(x[-1])
    
    c = Counter(labelList)
    tot = len(data)
    if (len(c) > 1):
        val1, count1 = c.most_common()[0]
        val2, count2 = c.most_common()[1]
        gin = 1 - pow(count1/tot, 2) - pow(count2/tot, 2)
        numOf = count1 + count2
    else :
        val1, count1 = c.most_common()[0]
        gin = 1 - pow(count1/tot, 2)
        numOf = count1

    print("feature: ", feat, " gini: ", gin)
    return gin, numOf

def chooseBestFeature(dataSet):
    '''
    choose best feature to split based on Gini index
    
    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    bestFeatId: int
        index of the best feature
    '''
    #TODO
    gin, kk = gini(dataSet)
    # print("gin: ", gin)
    tot = len(data)
    featLen = len(dataSet[0]) - 1
    for y in range(featLen) :
        giniCompiled = []
        countCompiled = []
        # print("INDEX: ", y)
        featList = []
        for x in dataSet:
            feat = x[y]
            featList.append(feat)
        featSet = set(featList)
        # print("featList: ", featList)
        # print("featSet: ", featSet)
        for z in featSet:
            ginList = []
            for k in dataSet:
                if z == k[y]:
                    ginList.append(k)
            # print("GINLIST: ", ginList)
            gingin, count = gini(ginList)
            giniCompiled.append(gingin)
            countCompiled.append(count)
        # print("giniCompiled: ", giniCompiled)
        # print("count Compied: ", countCompiled)
        gain = gin
        for g, c in zip(giniCompiled, countCompiled):
            gain = gain - ((c/tot) * g)
        print("INDEX: ", y, "GAIN: ", gain)
# use set on artificially made columns and then use that set to calculate the gini.
    bestFeatId = 0
    return bestFeatId  


def stopCriteria(dataSet):
    '''
    Criteria to stop splitting: 
    1) if all the classe labels are the same, then return the class label;
    2) if there are no more features to split, then return the majority label of the subset.

    Parameters
    -----------------
    dataSet: 2-D list
        [n_sampels, m_features + 1]
        the last column is class label

    Returns
    ------------------
    assignedLabel: string
        if satisfying stop criteria, assignedLabel is the assigned class label;
        else, assignedLabel is None 
    '''
    assignedLabel = None
    # TODO
    print("dataset: ", dataSet)
    labelList = []
    for x in dataSet:
        labelList.append(x[-1])

    # print("lab ", labelList)
    c = Counter(labelList)
    val, count = c.most_common()[0]
    # print("val: ", val)
    # print("count: ", count)
    assignedLabel = val

    return assignedLabel



def buildTree(dataSet, featNames):
    '''
    Build the decision tree

    Parameters
    -----------------
    dataSet: 2-D list
        [n'_sampels, m'_features + 1]
        the last column is class label

    Returns
    ------------------
        myTree: nested dictionary
    '''
    assignedLabel = stopCriteria(dataSet)
    # if assignedLabel:
    #     return assignedLabel
    bestFeatId = chooseBestFeature(dataSet)
    bestFeatName = featNames[bestFeatId]

    myTree = {bestFeatName:{}}
    subFeatName = featNames[:]
    del(subFeatName[bestFeatId])
    featValues = [d[bestFeatId] for d in dataSet]
    uniqueVals = list(set(featValues))
    for value in uniqueVals:
        myTree[bestFeatName][value] = buildTree(splitData(dataSet, bestFeatId, value), subFeatName)
    
    return myTree



if __name__ == "__main__":
    data, featNames = loadDataSet('golf.csv')
    dtTree = buildTree(data, featNames)
    # print (dtTree) 
    # treeplot.createPlot(dtTree)
    