import joblib


def apply(file_name, parameters=None):
    """
    Imports a MVP model

    Parameters
    ------------
    file_name
        File name
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    mvp
        MVP model
    """
    if parameters is None:
        parameters = {}

    return joblib.load(file_name)
