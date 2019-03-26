from pm4py.algo.discovery.massive_places.versions import first

MAX_NO_PLACES_EVALUATED = "max_no_places_evaluated"

FIRST = "first"

VERSIONS = {FIRST: first.apply}


def apply(log, parameters=None, variant=FIRST):
    return VERSIONS[variant](log, parameters=parameters)
