from pm4py.algo.mvp.exporter.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}

def apply(mvp, file_name, variant=CLASSIC, parameters=None):
    """
    Export a MVP model

    Parameters
    ------------
    mvp
        MVP model
    file_name
        File name
    variant
        Variant of the algorithm to apply
    parameters
        Parameters of the algorithm
    """
    return VERSIONS[variant](mvp, file_name, parameters=parameters)