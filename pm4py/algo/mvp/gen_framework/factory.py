from pm4py.algo.mvp.gen_framework.models import factory as model_factory
from pm4py.algo.mvp.gen_framework.rel_events import factory as rel_ev_factory
from pm4py.algo.mvp.gen_framework.rel_activities import factory as rel_act_factory
from pm4py.algo.mvp.gen_framework.node_freq import factory as node_freq_factory
from pm4py.algo.mvp.gen_framework.edge_freq import factory as edge_freq_factory

MODEL1 = model_factory.MODEL1
MODEL2 = model_factory.MODEL2
MODEL3 = model_factory.MODEL3
REL_DFG = rel_ev_factory.REL_DFG
BEING_PRODUCED = rel_ev_factory.BEING_PRODUCED
TYPE1 = node_freq_factory.TYPE1
TYPE11 = edge_freq_factory.TYPE11
TYPE12 = edge_freq_factory.TYPE12

COLORS = {REL_DFG: "#000000"}

def apply(df, model_type_variant=MODEL1, rel_ev_variant=REL_DFG, node_freq_variant=TYPE1, edge_freq_variant=TYPE11, parameters=None):
    if parameters is None:
        parameters = {}

    model = model_factory.apply(df, variant=model_type_variant)
    rel_ev = rel_ev_factory.apply(df, model, variant=rel_ev_variant)
    rel_act = rel_act_factory.apply(df, model, rel_ev)
    node_freq = node_freq_factory.apply(df, model, rel_ev, rel_act, variant=node_freq_variant)
    edge_freq = edge_freq_factory.apply(df, model, rel_ev, rel_act, variant=edge_freq_variant)

    model.set_rel_ev(rel_ev)
    model.set_rel_act(rel_act)
    model.set_node_freq(node_freq)
    model.set_edge_freq(edge_freq)

    return model