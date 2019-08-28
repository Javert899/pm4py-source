from pm4py.algo.mvp.gen_framework.rel_events import rel_dfg

REL_DFG = "rel_dfg"

VERSIONS = {REL_DFG: rel_dfg.apply}


def apply(df, variant=REL_DFG, parameters=None):
    if parameters is None:
        parameters = {}

    return VERSIONS[variant](df, parameters=parameters)
