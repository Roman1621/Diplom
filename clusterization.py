import numpy as np
from sklearn.cluster import KMeans
import mplcursors

def getClusterData(diction):
    cluster_data = {}

    for position, players in diction.items():
        for player_name, stats in players.items():
            for index, stat in enumerate(stats):
                if index not in cluster_data:
                    cluster_data[index] = []
                cluster_data[index].append((position, player_name, stat))
    
    return cluster_data

def clusterization(parameter1, parameter2, dct, ax, xlabel, ylabel, dir1, dir2, numberOfCl):
    data = getClusterData(dct)
    data_to_clusterX = np.array([item[2] for item in data[parameter1]])
    data_to_clusterY = np.array([item[2] for item in data[parameter2]])

    points = np.column_stack((data_to_clusterX, data_to_clusterY))
    reverse_indices = []
    if dir1 == 'По убыванию':
        reverse_indices.append(0)
    if dir2 == 'По убыванию':
        reverse_indices.append(1)
    n_points = normalize_data(points, reverse_indices)

    kmeans = KMeans(n_clusters=numberOfCl, random_state=0, n_init=10).fit(n_points)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    scatter = ax.scatter(n_points[:, 0], n_points[:, 1], c=labels, cmap='viridis')
    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=100, marker='')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    cursor = mplcursors.cursor(scatter, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(data[parameter1][sel.index][1]))
    cursor.connect("remove", lambda sel: sel.annotation.set_visible(False))
    ax.figure.colorbar(scatter)

    return labels, centroids, data[parameter1], data_to_clusterX, data_to_clusterY

def normalize_data(data, reverse_indices):
    max_values = np.max(data, axis=0)
    min_values = np.min(data, axis=0)
    for index in reverse_indices:
        data[:, index] = max_values[index] - data[:, index] + min_values[index]
    return data