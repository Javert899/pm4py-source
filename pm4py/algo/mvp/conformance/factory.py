from pm4py.algo.mvp.conformance.versions import list_models

LIST_MODELS = "list_models"

VERSIONS = {LIST_MODELS: list_models.apply}
VERSIONS_EVENT = {LIST_MODELS: list_models.apply_event}


def apply(model, df, variant=LIST_MODELS, parameters=None):
    """
    (Off-line) Conformance Checking of database event logs

    Parameters
    -------------
    model
        List of models
    df
        Database event log
    variant
        Variant of the algorithm
    parameters
        Parameters

    Returns
    -------------
    list_booleans
        List of booleans values, one per event, indicating if the execution of the event
        is fit according to the process model or not
    """
    return VERSIONS[variant](model, df, parameters=parameters)


def apply_event(model, event, current_status, variant=LIST_MODELS, parameters=None):
    """
    Conformance Checking of an event of a database event log given the models discovered for each perspective

    Parameters
    --------------
    model
        List of models
    event
        Database event
    current_status
        Current status of the execution
    variant
        Variant of the algorithm to apply
    parameters
        Parameters

    Returns
    --------------
    boolean
        Boolean value for event, indicating if the execution of the event is fit
    current_status
        Current status of the process model (updated with the new markings)
    problems
        List of class perspectives for which the replay has had some problem
    """
    return VERSIONS_EVENT[variant](model, event, current_status, parameters=parameters)
