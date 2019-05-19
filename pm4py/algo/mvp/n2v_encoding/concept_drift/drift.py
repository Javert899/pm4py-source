import numpy as np
from sklearn.decomposition import PCA

from pm4py.algo.mvp.n2v_encoding import encode


def apply(df, parameters=None):
    if parameters is None:
        parameters = {}

    encoding = parameters["encoding"] if "encoding" in parameters else encode.from_df(df, parameters=parameters)

    pca_components = parameters["pca_components"] if "pca_components" in parameters else 6
    min_rel_size_cluster = parameters["min_rel_size_cluster"] if "min_rel_size_cluster" in parameters else 0.05
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

    timestamps = {x["event_id"]: x["event_timestamp"] for x in
                 df[df["event_id"].isin(events_repr)][["event_id", "event_timestamp"]].to_dict("r")}
    print("timestamps=",timestamps)
    timest_list = [timestamps[x] for x in events_repr]
    print("timest_list=",timest_list)
    timest_list = np.asarray(timest_list)

    data2d = np.hstack((data2d, timest_list))

