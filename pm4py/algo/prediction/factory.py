import joblib

from pm4py.algo.prediction.versions import elasticnet, keras_rnn

ELASTICNET = "elasticnet"
KERAS_RNN = "keras_rnn"

VERSIONS_TRAIN = {ELASTICNET: elasticnet.train, KERAS_RNN: keras_rnn.train}
VERSIONS_TEST = {ELASTICNET: elasticnet.test, KERAS_RNN: keras_rnn.test}


def train(log, variant=ELASTICNET, parameters=None):
    """
    Train the prediction model

    Parameters
    -----------
    log
        Event log
    parameters
        Possible parameters of the algorithm
    variant
        Variant of the algorithm, possible values: elasticnet, keras_rnn
    Returns
    ------------
    model
        Trained model
    """
    return VERSIONS_TRAIN[variant](log, parameters=parameters)


def test(model, trace, parameters=None):
    """
    Test the prediction model

    Parameters
    ------------
    model
        Prediction model
    obj
        Object to predict (Trace / EventLog)
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    pred
        Result of the prediction (single value / list)
    """
    variant = model["variant"]
    return VERSIONS_TEST[variant](model, trace, parameters=parameters)


def save(model, filename):
    """
    Saves a model

    Parameters
    -------------
    model
        Prediction model
    filename
        Name of the file where to save the model
    """
    joblib.dump(model, filename, compress=3)


def load(filename):
    """
    Loads a model

    Parameters
    -------------
    filename
        Name of the file where the model is saved

    Returns
    -------------
    model
        Prediction model
    """
    return joblib.load(filename)
