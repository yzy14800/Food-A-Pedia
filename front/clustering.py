import numpy as np
from sklearn import cluster
from sklearn import metrics
from sklearn import preprocessing


def clustering(F):
    # normalize the Food Matrix
    nF = preprocessing.maxabs_scale(F, axis=0)
    C = cluster.SpectralClustering(
        n_clusters=25,
        eigen_solver='arpack',
        affinity="nearest_neighbors",
        n_neighbors=10
    )
    predict = C.fit_predict(nF)
    np.save('data/FOOD_CLS', predict)
    return predict


def belong2cluster(ndb_no, C, F, L):
    sample_no = indexOf(ndb_no, L)
    cluster = (C == C[sample_no])
    return F[cluster], L[cluster]


def indexOf(ndb_no, L):
    return np.nonzero(L == (int)(ndb_no))


def calSimilarity(cluster):
    return metrics.pairwise_distances(
        cluster,
        metric='cosine'
    )


def getSubstitute(ndb_no, C, F, L, n):
    c, l = belong2cluster(ndb_no, C, F, L)
    i = indexOf(ndb_no, l)
    S = calSimilarity(c)
    s = S[i].T
    I = np.argsort(-s, axis=0)
    return l[I[0:n, :]].ravel()

if __name__ == "__main__":
    F = np.load('data/FOOD_MAT.npy')
    L = np.load('data/FOOD_LAB.npy')
    # C=clustering(F)
    C = np.load('data/FOOD_CLS.npy')
    sub = getSubstitute('01012', C, F, L, 10)
    print(sub)
    sub = getSubstitute('17203', C, F, L, 10)
    print(sub)
    a = 1
