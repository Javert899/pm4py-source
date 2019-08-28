from pm4py.algo.mvp.gen_framework.rel_events import rel_dfg
from pm4py.algo.mvp.gen_framework.rel_events import being_produced

REL_DFG = "rel_dfg"
BEING_PRODUCED = "being_produced"

VERSIONS = {REL_DFG: rel_dfg.apply, BEING_PRODUCED: being_produced.apply}


def apply(df, variant=REL_DFG, parameters=None):
    if parameters is None:
        parameters = {}

    return VERSIONS[variant](df, parameters=parameters)
