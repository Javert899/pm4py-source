import numpy as np
from scipy.spatial import ConvexHull
from sklearn.decomposition import PCA

from pm4py.algo.mvp.n2v_encoding import encode


def apply(df, activity, parameters=None):
    if parameters is None:
        parameters = {}

    encoding = parameters["encoding"] if "encoding" in parameters else encode.from_df(df, parameters=parameters)

    pca_components = parameters["pca_components"] if "pca_components" in parameters else 3

    events = list(encoding["events"])
    events = [x for x in events if "activity="+str(activity) in x]

    print(len(events))

    data = []

    for event in events:
        data.append(encoding["model"][event])

    data = np.asarray(data)

    pca = PCA(n_components=pca_components)
    pca.fit(data)
    data2d = pca.transform(data)

    hull = ConvexHull(data2d)

    return [events[x] for x in hull.vertices]
