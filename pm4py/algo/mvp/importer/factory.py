from pm4py.algo.mvp.importer.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}

def apply(file_name, variant=CLASSIC, parameters=None):
    """
    Imports a MVP model

    Parameters
    ------------
    file_name
        File name
    variant
        Variant of the algorithm to apply
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    mvp
        MVP model
    """
    return VERSIONS[variant](file_name, parameters=parameters)
