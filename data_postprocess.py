import json

import numpy as np
import pandas as pd

import clustering


def get2json(subList, F, N, fields):
    json_str = []
    for ndb_no in subList:
        # get nutrient data
        record_n = N.loc[ndb_no, 1:2].transpose()
        json_n = record_n.to_json(orient='records')
        # get food description
        record_f = F.loc[ndb_no]
        json_f = record_f.to_json(orient='index')
        dict_f = json.loads(json_f)
        dict_f[fields[-1]] = json_n
        if len(str(ndb_no)) < 5:
            dict_f[fields[0]] = '0' + str(ndb_no)
        else:
            dict_f[fields[0]] = str(ndb_no)
        json_f = json.dumps(dict_f)
        print(json_f)
        json_str.append(json_f)
    json2 = '[' + ','.join(json_str) + ']'
    print(json2)
    return json2


def getNutrientName(DEF):
    return DEF.to_json(orient='index')


def getFoodGroup(GRP):
    return GRP.to_json(orient='index')


def getFood(ndb_no):
    FOOD_DES = pd.read_csv('data/FOOD_DES.csv', sep='^', header=None, names=['NDB_NO', 'LONG_DES', 'NUT_DATA'],
                           index_col=0, usecols=[0, 1, 2])
    f = FOOD_DES.loc[ndb_no]
    return f.to_json(orient='record')


def getFoodList(ndb_no):
    F = np.load('data/FOOD_MAT.npy')
    L = np.load('data/FOOD_LAB.npy')
    C = np.load('data/FOOD_CLS.npy')
    subList = clustering.getSubstitute(ndb_no, C, F, L, 10)
    fields = ['NDB_NO', 'GRP_CD', 'SHRT_DES', 'LONG_DES', 'NUT_DATA']
    FOOD_DES = pd.read_csv('data/FOOD_DES.csv', sep='^', header=None, names=fields[:4], index_col=0,
                           usecols=[0, 1, 2, 3])
    NUT_DATA = pd.read_csv('data/NUT_DATA.csv', sep='^', header=None, index_col=[0, 1])
    return get2json(subList, FOOD_DES, NUT_DATA, fields)


if __name__ == "__main__":
    fields = ['NDB_NO', 'GRP_CD', 'SHRT_DES', 'LONG_DES', 'NUT_DATA']
    FOOD_DES = pd.read_csv('data/FOOD_DES.csv', sep='^', header=None, names=fields[:4], index_col=0,
                           usecols=[0, 1, 2, 3])
    NUT_DATA = pd.read_csv('data/NUT_DATA.csv', sep='^', header=None, index_col=[0, 1])
    NUTR_DES = pd.read_csv('data/NUTR_DES.csv', sep='^', header=None, names=['NUT_CD', 'UNIT', 'NUT_NAME'], index_col=0,
                           usecols=[0, 1, 3])
    FD_GROUP = pd.read_csv('data/FD_GROUP.csv', sep='^', header=None, names=['GRP_CD', 'GRP_NAME'], index_col=0)
    F = np.load('data/FOOD_MAT.npy')
    L = np.load('data/FOOD_LAB.npy')
    C = np.load('data/FOOD_CLS.npy')
    sub = clustering.getSubstitute('01012', C, F, L, 10)
    j = get2json(sub, FOOD_DES, NUT_DATA, fields)
    a = 1
