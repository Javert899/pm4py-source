from pm4py.algo.mvp.places.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(df, mvp, variant=CLASSIC, parameters=None):
    """
    Gets a MVP model decorated by places and some Petri nets
    for the perspectives

    Parameters
    ------------
    df
        Dataframe
    mvp
        MVP model
    variant
        Variant of the algorithm, possible values: classic
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    mvp
        Possibly enriched MVP
    list_models
        List of Petri nets that were discovered
    """
    return VERSIONS[variant](df, mvp, parameters=parameters)
