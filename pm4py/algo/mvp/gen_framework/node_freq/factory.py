from pm4py.algo.mvp.gen_framework.node_freq import type1

TYPE1 = "type1"

VERSIONS = {TYPE1: type1.apply}


def apply(df, rel_ev, rel_act, variant=TYPE1, parameters=None):
    return VERSIONS[variant](df, rel_ev, rel_act, parameters=None)
