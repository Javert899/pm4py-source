from pm4py.algo.discovery.massive_places import factory as places_discovery
from pm4py.algo.mvp.projection.log import log_projection
from pm4py.objects.petri.utils import remove_transition
import traceback

def apply(df, mvp, parameters=None):
    """
    Gets a MVP model decorated by places and some Petri nets
    for the perspectives

    Parameters
    ------------
    df
        Dataframe
    mvp
        MVP model
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    mvp
        Possibly enriched MVP
    list_models
        List of Petri nets that were discovered
    """
    if parameters is None:
        parameters = {}

    list_models = {}

    for perspective in mvp:
        try:
            log = log_projection.get_perspective_filt_log_from_df_and_mvp_and_perspective(df, mvp, perspective)
            net, im, fm = places_discovery.apply(log)
            transitions = list(net.transitions)
            for trans in transitions:
                if len(trans.in_arcs) == 0 and len(trans.out_arcs) == 0:
                    net = remove_transition(net, trans)
            list_models[perspective] = net
            """mvp[perspective].data.append([])
            for place in net.places:
                preset_activities = []
                for arc in place.in_arcs:
                    source_trans = arc.source
                    preset_activities.append(source_trans.label)
                postset_activities = []
                for arc in place.out_arcs:
                    target_trans = arc.target
                    postset_activities.append(target_trans.label)
                mvp[perspective].data[-1].append((preset_activities, postset_activities, place))"""
            print("succeeded applying places discovery: ",perspective)
        except:
            print("exception in applying places discovery: ", perspective)
            traceback.print_exc()

    mvp = decorate_mvp_with_models(mvp, list_models)

    return mvp, list_models


def decorate_mvp_with_models(mvp, list_models):
    """
    Decorate a MVP model with formal models containing only places between visible transitions

    Parameters
    ------------
    mvp
        MVP model
    list_models
        List of models

    Returns
    ------------
    mvp
        Decorated MVP model
    """
    for persp in list_models:
        if persp in mvp:
            net = list_models[persp]
            mvp[persp].data.append([])
            for place in net.places:
                preset_activities = []
                for arc in place.in_arcs:
                    source_trans = arc.source
                    preset_activities.append(source_trans.label)
                postset_activities = []
                for arc in place.out_arcs:
                    target_trans = arc.target
                    postset_activities.append(target_trans.label)
                mvp[persp].data[-1].append((preset_activities, postset_activities, place))

    return mvp