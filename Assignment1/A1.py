import pandas as pd
import math as m
import csv
import random
import numpy
from csv import writer
from csv import reader
def Find_unique(data, col):     ##modify here
    return set([row[col] for row in data])

def match(data, col, val):
    value = data[col]
    return val == value


def info_gain(Yes, No, current):
    p = float(len(No)) / (len(No) + len(Yes))
    return current - p * Entropy(No) - (1 - p) * Entropy(Yes)


def Entropy(data):
    count = count_type(data)
    #print(count)
    E = 0
    for att in count:
        att_p = float(count[att]) / float(len(data))
        E += att_p * m.log(att_p,2)
    #print(-E)
    return -E

def count_type(data):
    count = {}
    for one_data in data:
        label = one_data[-1]
        if label not in count:
            count[label] = 0
        count[label] += 1
    return count

def separate(data, col, val):
    Yes, No= [], []
    for row in data:
        if match(row,col,val):
            Yes.append(row)
        else:
            No.append(row)
    return Yes, No

def generate_id(feature_num, subset_num):
    subset_id =[]
    for i in range(subset_num):
          r=random.randint(1,feature_num-1)
          if r not in subset_id: subset_id.append(r)
    return subset_id


def Split_point(data,percentageOfAttributes):


    highest_gain = 0
    best_question = None
    current = Entropy(data)
    best_col= 0
    feature_num = len(data[0]) - 1       #get number of features
    subset_num = int(m.ceil(feature_num * percentageOfAttributes))
    subset_id = generate_id(feature_num, subset_num)

#    print(subset_id)
    for col in range(feature_num):
        if col in subset_id:
            value = Find_unique(data, col)
        #print(col)
            for val in value:



                Yes_data, No_data = separate(data, col, val)
                if len(Yes_data) == 0 or len(No_data) == 0:
                    continue
                gain = info_gain(Yes_data, No_data, current)
            #print(question)
            #print(gain)
                if gain > highest_gain:
                    highest_gain, best_question, best_col = gain, val, col

    return highest_gain, best_question, best_col



class Leaf:

    def __init__(self, data):
        self.predictions = count_type(data)

class Node:
    def __init__(self,
                 att_name,
                 column,
                 Yes_branch,
                 No_branch):
        self.att_name = att_name
        self.column = column
        self.Yes_branch = Yes_branch
        self.No_branch = No_branch

def build_tree(data,percentageOfAttributes):

    gain, val, col = Split_point(data,percentageOfAttributes)

    if gain == 0:
        return Leaf(data)
    else:
        #print(val)
        #print(col)
        Yes, No = separate(data, col,val)
        Yes_branch = build_tree(Yes,percentageOfAttributes)
        No_branch = build_tree(No,percentageOfAttributes)

    return Node(val, col, Yes_branch, No_branch)


def test_result(row, node):

    if isinstance(node, Leaf):

        return node.predictions
    col = node.column
    val = node.att_name
    if match(row, col, val):

        return test_result(row, node.Yes_branch)
    else:
        return test_result(row, node.No_branch)

def print_leaf(counts):

    total = sum(counts.values())

    prob = {}

    for label in counts.keys():
        prob[label] = int(counts[label] )
    return prob

def TrainAndTestRandomForest(trainingdata, numberOfTrees, percentageOfAttributes, testdata):
    Yes_count = [0] * len(testdata)
    No_count = [0] * len(testdata)
    final_result = []
    for i in range(numberOfTrees):
        row_id = 0
        one_tree = build_tree(trainingdata,percentageOfAttributes)
        for row in testdata:
            tree_count = {}
            temp_max = 0
            a = print_leaf(test_result(row, one_tree))
            for label in a.keys():
                if a[label] > temp_max:
                    temp_max = a[label]
                    temp_label = label
            if temp_label in tree_count:
                tree_count[temp_label] += 1
            else:
                tree_count[temp_label] = 1

            #print(a)

            Yes_count, No_count = final_vote(row_id, tree_count,Yes_count, No_count)
            row_id+= 1
            #print(tree_count)
    for j in range(len(Yes_count)):
        if Yes_count[j]>No_count[j]:
            final_result.append('YES')
        else:
            final_result.append('NO')
    correct_predict = 0
    count = 0
    for col in testdata:

        if col[len(testdata[0])-1] == final_result[count]:
            correct_predict+=1
        #print(col[8])
        count+=1
    print('final_result: ',final_result)
    accuracy = (float(correct_predict)/float(len(testdata)))*100
    print('numberOfTrees: ', numberOfTrees)
    print('percentageOfAttributes: ', percentageOfAttributes*100,'%')
    print('Accuracy: ', accuracy,'%')
    return final_result



def final_vote(row_id, tree, Yes_count, No_count):
    #print(row_id)

    if 'YES' in tree.keys():
        Yes_count[row_id]+=1
    if 'NO' in tree.keys():
        No_count[row_id]+=1
    return Yes_count, No_count


with open('banks.csv', 'r') as f:

    dataset = list(csv.reader(f, delimiter=','))
training = dataset[1:]
#true_rows, false_rows, col = Split_point(training)
header = dataset[0:1]
with open('banks-test.csv', 'r') as t:
    testset = list(csv.reader(t, delimiter=','))
testing = testset[1:]


final_result = TrainAndTestRandomForest(training, 6, 0.5, testing)
ac
with open('banks-test.csv', 'r') as test, \
    open('predictions.csv', 'w' ,newline='') as predict:
    csv_reader  =  reader(test)
    csv_writer = writer(predict)
    count = 0
    for row in csv_reader:
        if count>=1:
            row.append(final_result[count-1])
            csv_writer.writerow(row)
        else:
            row.append('predictions')
            csv_writer.writerow(row)
        count+=1
