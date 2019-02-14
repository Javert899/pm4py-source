import numpy as np

from pm4py.algo.other.decisiontree import get_log_representation
from pm4py.algo.other.decisiontree import log_transforming
from pm4py.algo.other.decisiontree import mine_decision_tree
from pm4py.objects.bpmn.util import log_matching

DEFAULT_MAX_REC_DEPTH_DEC_MINING = 3


def perform_duration_root_cause_analysis_given_bpmn(log, bpmn_graph, bpmn_activity, parameters=None):
    """
    Perform root cause analysis about the excessive duration of an activity, matching the BPMN activities
    with the log.

    Parameters
    -------------
    log
        Trace log
    bpmn_graph
        BPMN graph that is being considered
    bpmn_activity
        Activity on the BPMN graph
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    clf
        Decision tree
    feature_names
        Feature names
    classes
        Classes
    """
    model_to_log, log_to_model = log_matching.get_log_match_with_model(log, bpmn_graph)
    log_activity = model_to_log[bpmn_activity]
    return perform_duration_root_cause_analysis(log, log_activity, parameters=parameters)


def get_data_classes_root_cause_analysis_given_bpmn(log, bpmn_graph, bpmn_activity, parameters=None):
    """
    Gets data and classes for root cause analysis about the excessive duration of an activity, matching the BPMN
    activities with the log.

    Parameters
    -------------
    log
        Trace log
    bpmn_graph
        BPMN graph that is being considered
    bpmn_activity
        Activity on the BPMN graph
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    data
        Data
    feature_names
        Feature names
    target
        Target for each example
    classes
        Classes
    """
    model_to_log, log_to_model = log_matching.get_log_match_with_model(log, bpmn_graph)
    log_activity = model_to_log[bpmn_activity]

    return get_data_classes_root_cause_analysis(log, log_activity, parameters=parameters)


def get_data_classes_root_cause_analysis(log, activity, parameters=None):
    """
    Gets data and classes for root cause analysis about the excessive duration of an activity

    Parameters
    -------------
    log
        Trace log
    activity
        Activity
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    data
        Data
    feature_names
        Feature names
    target
        Target for each example
    classes
        Classes
    """
    transf_log, traces_interlapsed_time_to_act = log_transforming.get_log_traces_until_activity(log, activity,
                                                                                                parameters=parameters)
    thresh = log_transforming.get_first_quartile_times_interlapsed_in_activity(log, activity, parameters=parameters)
    data, feature_names = get_log_representation.get_default_representation(transf_log)
    classes = ["under", "over"]
    target = []
    for it in traces_interlapsed_time_to_act:
        if it <= thresh:
            target.append(0)
        else:
            target.append(1)
    target = np.array(target)

    return data, feature_names, target, classes


def perform_duration_root_cause_analysis(log, activity, parameters=None):
    """
    Perform root cause analysis about the excessive duration of an activity

    Parameters
    -------------
    log
        Trace log
    activity
        Activity
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    clf
        Decision tree
    feature_names
        Feature names
    classes
        Classes
    """

    data, feature_names, target, classes = get_data_classes_root_cause_analysis(log, activity, parameters=parameters)

    clf = mine_decision_tree.mine(data, target, max_depth=DEFAULT_MAX_REC_DEPTH_DEC_MINING)

    return clf, feature_names, classes
