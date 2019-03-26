from pm4py.algo.discovery.complex_discovery.versions import first

FIRST = "first"

VERSIONS = {FIRST: first.apply}


def apply(log, variant=FIRST, parameters=None):
    return VERSIONS[variant](log, parameters=parameters)
