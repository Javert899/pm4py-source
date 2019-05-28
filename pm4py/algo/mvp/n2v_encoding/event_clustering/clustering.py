import numpy as np
from sklearn.cluster import Birch
from sklearn.decomposition import PCA

from pm4py.algo.mvp.n2v_encoding import encode


def apply(df, parameters=None):
    """
    Algorithm to apply clustering to database event log

    Parameters
    ------------
    df
        Dataframe representing the database event log
    parameters
        Parameters of the algorithm

    Returns
    ------------
    list_dataframes
        List of dataframes that are the clusters detected by the algorithm
    """
    if parameters is None:
        parameters = {}

    encoding = parameters["encoding"] if "encoding" in parameters else encode.from_df(df, parameters=parameters)

    pca_components = parameters["pca_components"] if "pca_components" in parameters else 3
    no_clusters = parameters["no_clusters"] if "no_clusters" in parameters else 2

    events = list(encoding["events"])

    data = []

    for event in events:
        data.append(encoding["model"][event])

    data = np.asarray(data)

    pca = PCA(n_components=pca_components)
    pca.fit(data)
    data2d = pca.transform(data)

    db = Birch(n_clusters=no_clusters).fit(data2d)
    labels = db.labels_

    already_seen = {}
    clusters_list = []

    for i in range(len(events)):
        if not labels[i] in already_seen:
            already_seen[labels[i]] = len(list(already_seen.keys()))
            clusters_list.append([])
        clusters_list[already_seen[labels[i]]].append(events[i].split("event=")[1].split(" activity=")[0])

    dataframes_list = []

    for cl in clusters_list:
        dataframes_list.append(df[df["event_id"].isin(cl)])

    return dataframes_list
