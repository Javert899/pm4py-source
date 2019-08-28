from pm4py.algo.mvp.gen_framework.edge_freq import type11, type12

TYPE11 = "type11"
TYPE12 = "type12"

VERSIONS = {TYPE11: type11.apply, TYPE12: type12.apply}


def apply(df, rel_ev, rel_act, variant=TYPE11, parameters=None):
    return VERSIONS[variant](df, rel_ev, rel_act, parameters=parameters)
