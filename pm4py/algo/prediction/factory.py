from pm4py.algo.prediction.versions import elasticnet

ELASTICNET = "elasticnet"

VERSIONS_TRAIN = {ELASTICNET: elasticnet.train}
VERSIONS_TEST = {ELASTICNET: elasticnet.test}


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
        Variant of the algorithm, possible values: elasticnet
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
