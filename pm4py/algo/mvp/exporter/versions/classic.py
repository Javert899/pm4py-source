import joblib


def apply(mvp, file_name, parameters=None):
    """
    Export a MVP model

    Parameters
    ------------
    mvp
        MVP model
    file_name
        File name
    parameters
        Parameters of the algorithm
    """
    if parameters is None:
        parameters = {}

    joblib.dump(mvp, file_name, compress=3)
