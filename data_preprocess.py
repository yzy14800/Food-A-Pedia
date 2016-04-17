import os.path

import numpy as np
from sklearn import preprocessing


def extractRawData(fname):
    npy = 'data' + fname.strip('sr22').replace('txt', 'npy')
    if os.path.exists(npy):
        raw_data = np.load(npy)
    else:
        raw_data = np.genfromtxt(
            fname,
            delimiter='^'
            , dtype=None
            , filling_values=0
            , comments=None
        )
        np.save(npy, raw_data)
    # for d in raw_data:
    #     for f in d:
    #         if f.dtype.type is np.string_:
    #             f=bytes(f.decode('utf-8').strip('~'),'utf-8')
    #             a=1
    return raw_data


def raw2csv(raw_name, csv_name):
    with open(csv_name, 'a') as output:
        with open(raw_name, 'r') as input:
            for line in input:
                output.write(line.replace('~', '').replace('^', ';'))

def constructFoodMatrix(food_des, nut_data, nutr_def):
    # get the number of nutrition types
    max_nutr_no = 0
    for n in nutr_def:
        nutr_no = (int)(n[0].decode('utf-8').strip('~'))
        if max_nutr_no < nutr_no:
            max_nutr_no = nutr_no

    # get the labels of food
    food_labels = []
    for f in food_des:
        ndb_no = f[0].decode('utf-8').strip('~')
        food_labels.append(ndb_no)
    np.save('data/FOOD_LAB', np.array(food_labels))

    # construct food matrix
    F = np.zeros((food_des.size, max_nutr_no), dtype=float)
    for n in nut_data:
        ndb_no = n[0].decode('utf-8').strip('~')
        nutr_no = (int)(n[1].decode('utf-8').strip('~')) - 1
        row = food_labels.index(ndb_no)
        F[row, nutr_no] = n[2]
    np.save('data/FOOD_MAT', F)


def normalizeFoodMatrix(F):
    nF0 = preprocessing.maxabs_scale(F, axis=0)
    a = 0

if __name__ == "__main__":
    # food_des = extractRawData('sr22/FOOD_DES.txt')
    # nut_data = extractRawData('sr22/NUT_DATA.txt')
    # nutr_def = extractRawData('sr22/NUTR_DEF.txt')
    # constructFoodMatrix(food_des, nut_data,nutr_def)
    # food_labels=np.load('data/FOOD_LAB.npy')
    # F = np.load('data/FOOD_MAT.npy')
    # nF=normalizeFoodMatrix(F)
    fname = ['FOOD_DES', 'NUT_DATA', 'FD_GROUP', 'NUTR_DEF', 'WEIGHT',
             'FOOTNOTE', 'DATA_SRC', 'DATSRCLN', 'DERIV_CD', 'SRC_CD']
    for f in fname:
        raw2csv('sr22/' + f + '.txt', 'data/' + f + '.csv')
