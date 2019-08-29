from pm4py.algo.mvp.gen_framework.rel_events import rel_dfg
from pm4py.algo.mvp.gen_framework.rel_events import being_produced
from pm4py.algo.mvp.gen_framework.rel_events import existence
from pm4py.algo.mvp.gen_framework.rel_events import link

REL_DFG = "rel_dfg"
BEING_PRODUCED = "being_produced"
EXISTENCE = "existence"
LINK = "link"

VERSIONS = {REL_DFG: rel_dfg.apply, BEING_PRODUCED: being_produced.apply, EXISTENCE: existence.apply, LINK: link.apply}


def apply(df, model, variant=REL_DFG, parameters=None):
    if parameters is None:
        parameters = {}

    return VERSIONS[variant](df, model, parameters=parameters)
