import pandas as pd
import math as m
import csv
import random
import numpy
from csv import writer
from csv import reader
import copy
with open('agaricus-lepiota.csv', 'r') as f:

    dataset = list(csv.reader(f, delimiter=','))
    #print(dataset[0:])
    missing_count = 0

    for row in dataset:
        position = 0
        for missing in row:
            if not missing.isalpha():

                missing_count+=1
                #print(missing)
                continue

    print("missing entry:",missing_count)

    print("Total rows:",len(dataset))
#test_data = dataset[0:8]
#print(test_data)
#print(dataset[0])
#


def count_type(data):
    total = 0
    count = {}
    for one_data in data:
        label = one_data[11]
        total+=1
        if label not in count:
            count[label] = 0
        count[label] += 1
    return count, total

def kmodes(dataset, numberOfClusters):
    cluster = random.sample(dataset, numberOfClusters)
    #print(cluster)

    d = init_centroid(dataset,  cluster)    # centroid initialization & assign observation to cluster
    cluster_distance = max_distance(dataset, cluster)
    #cluster = copy.copy(repeat_cluster(d,numberOfClusters))

    print("Error rate:",cluster_distance/8124/23)
    #print(d)
    #print(cluster)
    final_distance = 0

    while(True):


        #print(i)
        cluster = copy.copy(repeat_cluster(d,numberOfClusters)) # generate new centroids
        #print(cluster)
        d = []
        d = copy.copy(init_centroid(dataset,  cluster))
        cluster_distance = max_distance(dataset, cluster)
        #print(d)
        if cluster_distance == final_distance: # Terminating critieria: if false rate doesnt decrease then stop
            break
        else:

            final_distance = cluster_distance
        print("Error rate:",cluster_distance/8124/23)

    return d

def max_distance(dataset, cluster):
    length = len(cluster[0])

    distance = 0
    for row in dataset:
        max_count = m.inf

        for Acluster in cluster:
            count = 0
            for j in range(length):
                if Acluster[j] != row[j]:
                    count +=1
            if count < max_count:
                max_count = count

        distance+= max_count
    return distance

def init_centroid(dataset, cluster):
    length = len(cluster[0])
    new = []
    Arow = []
    for row in dataset:
        max_count = m.inf
        cluster_count = 0
        for Acluster in cluster:

            count = 0

            #print(len(Acluster))
            #print(Acluster)
            for j in range(length):
                if Acluster[j] != row[j]:
                    count +=1

            if count < max_count:
                max_count = count
                cluster_num = cluster_count
            cluster_count +=1
        Arow = copy.deepcopy(row)
        Arow.append(cluster_num)

        new.append(Arow)

    return new

def repeat_cluster(data,numberOfClusters):
    length = len(data[0])-1
    cluster_table = []
    #print(data[0][length])
    for i in range(numberOfClusters):
        temp_cluster = []
        for row in data:
            if row[length] == i:
                temp_cluster.append(row)




        column_table = []
        for i in range(length):
            columns = []
            for temp_r in  temp_cluster:
                columns.append(temp_r[i])
            column_table.append(columns)

        #print(column_table)
        #print("DDDDDDDDDDDDDDDDDDDDDD")
        One_cluster = most_frequent(column_table)

        cluster_table.append(One_cluster)
    #print(cluster_table)

    return cluster_table



def most_frequent(List):

    cluster = []
    for j in range(len(List)):
        one_col = List[j]
        counter = 0
        for i in one_col:
            curr_frequency = one_col.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
        cluster.append(num)
    return cluster


def data_cleaning(data, distribution,total):

    for row in data:
        position = 0
        label = row[11]
        if not label.isalpha():
            #print(missing)
            row[11] = fuilling(distribution,total)

            continue



    return data


def fuilling(distribution,total):
    legal_entry = 0
    for key in distribution:
        if key.isalpha():
            legal_entry+=   distribution[key]
    rad = random.randint(0,legal_entry)
    for key in distribution:
        if distribution[key]-rad > 0:
            return key
        rad = rad - distribution[key]
    return None









distribution, total  = count_type(dataset)
dataset = data_cleaning(dataset, distribution,total)  #data preparing

d = kmodes(dataset,23)



with open('cluster.csv', 'w',newline='') as cluster:            # Saving results to a file
    wr = csv.writer(cluster,delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for row in dataset:
        wr.writerow(row)
