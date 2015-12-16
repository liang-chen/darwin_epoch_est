
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from myClass import mGaussian
from math import log
import random

def get_kl_dist(list_p,list_q):
    return sum([p*log(p/q,2) for p,q in zip(list_p, list_q)])

def get_mean_cols(matrix):
    s = []
    for i in xrange(len(matrix)):
        if len(s) == 0:
            s = matrix[i]
        else:
            s = [x+y for x,y in zip(s, matrix[i])]
    if len(s):
        s = [x/len(matrix) for x in s]
    #print 'haha'
    #print(sum(s))
    return s

def KL_pair_trivial(KL_matrix):
    pList = []
    for i in xrange(len(KL_matrix)):
        row = KL_matrix[i,:]

        local_kl = i + random.random()/10 
        global_kl = i + random.random()/10
        pList.append([local_kl, global_kl])
    pairs = np.array(pList)
    return pairs

def KL_pair(KL_matrix, Topics_matrix):
    pList = []
    global_kl = []
    
    if(len(Topics_matrix) == 0):
        return np.array([])
    
    past = [1.0/ len(Topics_matrix[0,])]*len(Topics_matrix[0,])
    for i in xrange(len(Topics_matrix)):
        cur = Topics_matrix[i,]
        global_kl.append(get_kl_dist(cur, past))
        past = get_mean_cols(Topics_matrix[0:i+1])
    
    for i in xrange(len(KL_matrix)):
        row = KL_matrix[i,:]
        if(i == 0):
            local_kl = 0
        #global_kl = 0
        else:
            local_kl = row[i-1]
        #global_kl = sum(row[:i])/i
        pList.append([local_kl, global_kl[i]])
    pairs = np.array(pList)
    return pairs

def KMC(pairs, n): #kmeans clustering on kl distance pairs
    k_means = KMeans(init='k-means++', n_clusters=n, n_init=10)
    k_means.fit(pairs)
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)
    colors = ['#4EACC5', '#FF9C34', '#4E9A06', '#FFD700', '#00FF7F', '#B22222', '#D02090', '#EED5B7']

    # KMeans Plot
    fig = plt.figure(figsize=(8, 3))
    ax = fig.add_subplot(1,1,1)
    for k, col in zip(range(n), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(pairs[my_members, 0], pairs[my_members, 1], 'w', markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

    plt.show()
    return k_means

def learn_KL_gaussian(k_means, pairs):
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    n = k_means.n_clusters
    kGaussians = []
    for k in range(n):
        my_members = k_means_labels == k
        my_center = sum(pairs[my_members,:]) / len(pairs[my_members,:])#k_means_cluster_centers[k]
        my_data = pairs[my_members,:]
        my_cov = np.cov(my_data, rowvar = 0)
        #print my_cov
        kGaussians.append(mGaussian(my_center, my_cov))
    return kGaussians

def learn_from_KL(KL_matrix, Topics_matrix, n):
    pairs = KL_pair(KL_matrix, Topics_matrix)
    k_means_list = []

    for i in xrange(2, n+1):
        k_means_list.append(KMC(pairs, i))

    #k_means_t = KMC(pairs_t, n)
    kGaussians = []
    for k_means in k_means_list:
        kGaussians = kGaussians + learn_KL_gaussian(k_means, pairs)
    return pairs, np.array(kGaussians)
