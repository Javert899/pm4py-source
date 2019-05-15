from pm4py.objects.bpmn.util import gateway_map as gwmap_builder
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.log.util import get_log_representation, get_prefixes
from pm4py.objects.log.log import EventLog
import itertools
import traceback
from copy import deepcopy
from pm4py.algo.other.anchors import factory as anchors_factory
import logging


def get_anchors_from_log_and_bpmn_graph(log, bpmn_graph, parameters=None):
    """
    Get the anchors for gateways from a log and a BPMN graph

    Parameters
    ------------
    log
        Event log
    bpmn_graph
        BPMN graph
    parameters
        Parameters of the algorithm

    Returns
    -------------
    anchors_map
        Map that associates to each gateway an anchor
    """
    if parameters is None:
        parameters = {}

    consider_all_elements_to_be_task = parameters[
        "consider_all_elements_to_be_task"] if "consider_all_elements_to_be_task" in parameters else False
    use_node_id = parameters["use_node_id"] if "use_node_id" in parameters else False
    relax_condition_one_entry = parameters[
        "relax_condition_one_entry"] if "relax_condition_one_entry" in parameters else True

    gateway_map, edges_map = gwmap_builder.get_gateway_map(bpmn_graph,
                                                           consider_all_elements_to_be_task=consider_all_elements_to_be_task,
                                                           use_node_id=use_node_id,
                                                           relax_condition_one_entry=relax_condition_one_entry)

    return get_anchors_from_log_and_gwmap(log, gateway_map, parameters=parameters)


def get_anchors_from_log_and_gwmap(log, gateway_map, parameters=None):
    """
    Get the anchors for gateways from a log and a gateway map

    Parameters
    -------------
    log
        Event log
    gateway_map
        Gateway map
    parameters
        Parameters of the algorithm

    Returns
    -------------
    anchors_map
        Map that associates to each gateway an anchor
    """
    if parameters is None:
        parameters = {}

    ret_map = {}

    for gw in gateway_map:
        try:
            source_activity = gateway_map[gw]["source"]
            if gateway_map[gw]["type"] == "onlytasks":
                target_activities = [x for x in gateway_map[gw]["edges"]]
                anchors = get_anchors_given_activities(log, target_activities, parameters=parameters)
                ret_map[gw] = anchors
            else:
                main_target_activity = list(gateway_map[gw]["edges"].keys())[0]
                other_activities = get_other_activities_connected_to_source(log, source_activity, main_target_activity)
                if other_activities:
                    target_activities = [main_target_activity] + other_activities
                    anchors = get_anchors_given_activities(log, target_activities, parameters=parameters)
                    ret_map[gw] = anchors
        except:
            # traceback.print_exc()
            pass

    return ret_map


def get_other_activities_connected_to_source(log, source_activity, main_target_activity, parameters=None):
    """
    Gets the other activities connected to the source activity

    Parameters
    ------------
    log
        Trace log
    source_activity
        Source activity
    main_target_activity
        Main target activity
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    other_activities
        Other activities connected to the source
    """
    other_activities = []
    dfgk = list(dfg_factory.apply(log, parameters=parameters).keys())
    for key in dfgk:
        if key[0] == source_activity:
            target_activity = key[1]
            if not target_activity == main_target_activity:
                other_activities.append(target_activity)
    return other_activities


def get_anchors_given_activities(log, activities, parameters=None):
    """
    Performs decision mining on the causes the leads to an exclusive choice of the activities

    Parameters
    -------------
    log
        Trace log
    activities
        List of activities to consider in decision mining
    parameters
        Possible parameters of the algorithm, including:
            PARAMETER_CONSTANT_ACTIVITY_KEY -> activity
            PARAMETER_CONSTANT_TIMESTAMP_KEY -> timestamp

    Returns
    -------------
    anchors
        Anchors object
    """
    if parameters is None:
        parameters = {}

    max_diff_targets = parameters["max_diff_targets"] if "max_diff_targets" in parameters else 9999999999

    list_logs, considered_activities = get_prefixes.get_log_traces_to_activities(log, activities,
                                                                                 parameters=parameters)

    classes = considered_activities
    target = []
    for i in range(len(list_logs)):
        target = target + [min(i, max_diff_targets)] * len(list_logs[i])

    transf_log = EventLog(list(itertools.chain.from_iterable(list_logs)))

    anchors = anchors_factory.apply(transf_log, target, classes, parameters=parameters)
    anchors.train()

    return anchors
