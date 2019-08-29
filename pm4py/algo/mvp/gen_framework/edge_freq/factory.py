from pm4py.algo.mvp.gen_framework.edge_freq import type11, type12, type13, type211

TYPE11 = "type11"
TYPE12 = "type12"
TYPE13 = "type13"
TYPE211 = "type211"

VERSIONS = {TYPE11: type11.apply, TYPE12: type12.apply, TYPE13: type13.apply, TYPE211: type211.apply}


def apply(df, model, rel_ev, rel_act, variant=TYPE11, parameters=None):
    return VERSIONS[variant](df, model, rel_ev, rel_act, parameters=parameters)
