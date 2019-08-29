from pm4py.algo.mvp.gen_framework.node_freq import type1, type21, type22, type23

TYPE1 = "type1"
TYPE21 = "type21"
TYPE22 = "type22"
TYPE23 = "type23"

VERSIONS = {TYPE1: type1.apply, TYPE21: type21.apply, TYPE22: type22.apply, TYPE23: type23.apply}


def apply(df, model, rel_ev, rel_act, variant=TYPE1, parameters=None):
    return VERSIONS[variant](df, model, rel_ev, rel_act, parameters=parameters)
