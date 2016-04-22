import numpy as np
from sklearn import cluster
from sklearn import preprocessing


def clustering(F):
    # normalize the Food Matrix
    nF = preprocessing.maxabs_scale(F, axis=0)
    C = cluster.SpectralClustering(
        n_clusters=25,
        affinity='nearest_neighbors',
        n_neighbors=10
    )
    predict = C.fit_predict(nF)
    np.save('data/FOOD_CLS', predict)
    return predict


def belong2cluster(sample_no, C, F, L):
    cluster = (C == C[sample_no])
    return F[cluster], L[cluster]


if __name__ == "__main__":
    F = np.load('data/FOOD_MAT.npy')
    L = np.load('data/FOOD_LAB.npy')
    # C=clustering(F)
    C = np.load('data/FOOD_CLS.npy')
    c, l = belong2cluster(12, C, F, L)
    a = 1
