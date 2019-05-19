import numpy as np
from scipy.spatial import ConvexHull
from sklearn.decomposition import PCA

from pm4py.algo.mvp.n2v_encoding import encode


def apply(df, ob_class, parameters=None):
    """
    Gets the vertices of the convex hull of the objects belonging to a given class

    Parameters
    -----------
    df
        Dataframe
    ob_class
        Object class
    parameters
        Parameters of the algorithm

    Returns
    ------------
    vertices
        Vertices of the convex hull
    """
    if parameters is None:
        parameters = {}

    encoding = parameters["encoding"] if "encoding" in parameters else encode.from_df(df, parameters=parameters)

    pca_components = parameters["pca_components"] if "pca_components" in parameters else 3

    objects = list(encoding["objects"])
    objects = [x for x in objects if "class="+str(ob_class) in x]

    data = []

    for object in objects:
        data.append(encoding["model"][object])

    data = np.asarray(data)

    pca = PCA(n_components=pca_components)
    pca.fit(data)
    data2d = pca.transform(data)

    hull = ConvexHull(data2d)

    return [objects[x] for x in hull.vertices]
