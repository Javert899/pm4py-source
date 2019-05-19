from statistics import median

import numpy as np
from sklearn.cluster import Birch
from sklearn.decomposition import PCA

from pm4py.algo.mvp.n2v_encoding import encode


def first_quartile(values):
    idx = int(float(len(values)) * 1.0 / 4.0)
    return values[idx]


def third_quartile(values):
    idx = int(float(len(values)) * 3.0 / 4.0)
    return values[idx]


def apply(df, parameters=None):
    """
    Algorithm to detect concept drift in a database event log

    Parameters
    ------------
    df
        Dataframe representing the database event log
    parameters
        Parameters of the algorithm

    Returns
    ------------
    list_dataframes
        List of dataframes that shows separation among features
    """
    if parameters is None:
        parameters = {}

    encoding = parameters["encoding"] if "encoding" in parameters else encode.from_df(df, parameters=parameters)

    pca_components = parameters["pca_components"] if "pca_components" in parameters else 6
    min_n_clusters_to_search = parameters["min_n_clusters_to_search"] if "min_n_clusters_to_search" in parameters else 2
    max_n_clusters_to_search = parameters["max_n_clusters_to_search"] if "max_n_clusters_to_search" in parameters else 5

    events = list(encoding["events"])
    events_repr = [x.split("event=")[1].split(" activity=")[0] for x in events]

    data = []

    for event in events:
        data.append(encoding["model"][event])

    data = np.asarray(data)

    pca = PCA(n_components=pca_components)
    pca.fit(data)
    data2d = pca.transform(data)

    timestamps = {x["event_id"]: x["event_timestamp"].timestamp() for x in
                 df[df["event_id"].isin(events_repr)][["event_id", "event_timestamp"]].to_dict("r")}
    min_timestamp = min(timestamps.values())
    max_timestamp = max(timestamps.values())
    inv_diff_timestamps = 1.0 / (max_timestamp - min_timestamp)
    timest_list = [(timestamps[x] - min_timestamp)*inv_diff_timestamps for x in events_repr]
    timest_list = np.transpose(np.asmatrix(timest_list))

    data2d = np.hstack((data2d, timest_list))

    for cluster_size in range(min_n_clusters_to_search, max_n_clusters_to_search + 1):
        db = Birch(n_clusters=cluster_size).fit(data2d)
        labels = db.labels_

        already_seen = {}
        clusters_list = []

        for i in range(len(events)):
            if not labels[i] in already_seen:
                already_seen[labels[i]] = len(list(already_seen.keys()))
                clusters_list.append([])
            event_label = events[i].split("event=")[1].split(" activity=")[0]
            clusters_list[already_seen[labels[i]]].append([event_label, timestamps[event_label]])

        clusters_list = sorted(clusters_list, key=lambda x: median(y[1] for y in x))

        ok = True

        for i in range(len(clusters_list)-1):
            c1 = clusters_list[i]
            c2 = clusters_list[i+1]

            v1 = sorted(list(v[1] for v in c1))
            v2 = sorted(list(v[1] for v in c2))

            if third_quartile(v1) >= first_quartile(v2):
                ok = False
                break

        if ok:
            dataframes_list = []

            for cl0 in clusters_list:
                cl = [x[0] for x in cl0]
                dataframes_list.append(df[df["event_id"].isin(cl)])

            return dataframes_list

    return []
