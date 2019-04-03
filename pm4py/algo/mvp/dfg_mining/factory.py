from pm4py.algo.mvp.dfg_mining.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(mvp, variant=CLASSIC, parameters=None):
    """
    Apply DFG mining

    Parameters
    ------------
    mvp
        Multiple Viewpoint Model
    variant
        Variant of the algorithm to apply, possible values: classic
    parameters
        Parameters of the algorithm

    Returns
    ------------
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    """
    return VERSIONS[variant](mvp, parameters=parameters)
