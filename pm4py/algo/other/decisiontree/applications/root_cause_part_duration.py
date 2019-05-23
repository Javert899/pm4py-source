import numpy as np
from sklearn import tree

from pm4py.objects.bpmn.util import log_matching
from pm4py.objects.log.util import get_log_representation, get_prefixes
from pm4py.objects.log.util import xes
from pm4py.util import constants
import logging

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
    transf_log, traces_interlapsed_time_to_act = get_prefixes.get_log_traces_until_activity(log, activity,
                                                                                            parameters=parameters)
    thresh = get_first_quartile_times_interlapsed_in_activity(log, activity, parameters=parameters)
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

    clf = tree.DecisionTreeClassifier(max_depth=DEFAULT_MAX_REC_DEPTH_DEC_MINING)
    clf.fit(data, target)

    return clf, feature_names, classes


def get_all_interlapsed_times_in_activity(log, activity, parameters=None):
    """
    Gets all the interlapsed times in an activity

    Parameters
    ------------
    log
        Trace log object
    activity
        Activity
    parameters
        Possible parameters of the algorithm, including:
            PARAMETER_CONSTANT_ACTIVITY_KEY -> activity
            PARAMETER_CONSTANT_TIMESTAMP_KEY -> timestamp

    Returns
    ------------
    interlapsed_times
        All interlapsed times in the activity
    """

    if parameters is None:
        parameters = {}

    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    timestamp_key = parameters[
        constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] if constants.PARAMETER_CONSTANT_TIMESTAMP_KEY in parameters else xes.DEFAULT_TIMESTAMP_KEY

    interlapsed_times = []

    i = 0
    while i < len(log):
        ev_in_tr_w_act = sorted([j for j in range(len(log[i])) if log[i][j][activity_key] == activity])
        if ev_in_tr_w_act and ev_in_tr_w_act[0] > 0:
            try:
                interlapsed_times.append(
                    log[i][ev_in_tr_w_act[0]][timestamp_key].timestamp() - log[i][ev_in_tr_w_act[0] - 1][
                        timestamp_key].timestamp())
            except:
                interlapsed_times.append(
                    log[i][ev_in_tr_w_act[0]][timestamp_key] - log[i][ev_in_tr_w_act[0] - 1][
                        timestamp_key])
                logging.error("timestamp_key not timestamp")
        i = i + 1

    interlapsed_times = sorted(interlapsed_times)

    return interlapsed_times


def get_first_quartile_times_interlapsed_in_activity(log, activity, parameters=None):
    """
    Gets the first quartile of times interlapsed in an activity

    Parameters
    ------------
    log
        Trace log
    activity
        Activity
    parameters
        Possible parameters of the algorithm, including:
            PARAMETER_CONSTANT_ACTIVITY_KEY -> activity
            PARAMETER_CONSTANT_TIMESTAMP_KEY -> timestamp

    Returns
    -------------
    stat
        Statistic value
    """
    stat = 0

    interlapsed_times = get_all_interlapsed_times_in_activity(log, activity, parameters=parameters)

    if interlapsed_times:
        stat = interlapsed_times[int(3 * len(interlapsed_times) / 4)]

    return stat
