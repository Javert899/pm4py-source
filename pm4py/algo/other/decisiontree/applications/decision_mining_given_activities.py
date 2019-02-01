import itertools
import traceback
from copy import deepcopy

import numpy as np

from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.algo.other.decisiontree import get_log_representation
from pm4py.algo.other.decisiontree import log_transforming
from pm4py.algo.other.decisiontree import mine_decision_tree
from pm4py.objects.bpmn.util import gateway_map as gwmap_builder
from pm4py.objects.bpmn.util import log_matching
from pm4py.objects.log.log import EventLog

DEFAULT_MAX_REC_DEPTH_DEC_MINING = 2


def get_rules_per_edge_given_bpmn(log, bpmn_graph, parameters=None):
    """
    Gets the rules associated to each edge, matching the BPMN activities with the log.

    Parameters
    ------------
    log
        Trace log
    bpmn_graph
        BPMN graph that is being considered
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    rules_per_edge
        Dictionary that associates to each edge a rule
    """
    gateway_map, edges_map = gwmap_builder.get_gateway_map(bpmn_graph)

    return get_rules_per_edge_given_bpmn_and_gw_map(log, bpmn_graph, gateway_map, parameters=parameters)


def get_rules_per_edge_given_bpmn_and_gw_map(log, bpmn_graph, gateway_map, parameters=None):
    """
    Gets the rules associated to each edge, matching the BPMN activities with the log.

    Parameters
    ------------
    log
        Trace log
    bpmn_graph
        BPMN graph that is being considered
    gateway_map
        Gateway map
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    rules_per_edge
        Dictionary that associates to each edge a rule
    """
    model_to_log, log_to_model = log_matching.get_log_match_with_model(log, bpmn_graph)
    gmk = list(gateway_map.keys())
    for gw in gmk:
        try:
            gateway_map[gw]["source"] = model_to_log[gateway_map[gw]["source"]]
            for n in gateway_map[gw]["edges"]:
                gmgwk = gateway_map[gw]["edges"].keys()
                for key in gmgwk:
                    if not key == model_to_log[key]:
                        gateway_map[gw]["edges"][n][model_to_log[key]] = gateway_map[gw]["edges"][n][key]
                        del gateway_map[gw]["edges"][n][key]
        except:
            traceback.print_exc()
            del gateway_map[gw]

    return get_rules_per_edge(log, gateway_map, parameters=parameters)


def get_rules_per_edge(log, gateway_map, parameters=None):
    """
    Gets the rules associated to each edge

    Parameters
    ------------
    log
        Trace log
    gateway_map
        Gateway map
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    rules_per_edge
        Dictionary that associates to each edge a rule
    """
    rules_per_edge = {}
    for gw in gateway_map:
        rules = None
        rules = {}
        source_activity = gateway_map[gw]["source"]
        if gateway_map[gw]["type"] == "onlytasks":
            target_activities = [x for x in gateway_map[gw]["edges"]]
            rules = get_decision_mining_rules_given_activities(log, target_activities, parameters=parameters)
        else:
            main_target_activity = list(gateway_map[gw]["edges"].keys())[0]
            other_activities = get_other_activities_connected_to_source(log, source_activity, main_target_activity)
            if other_activities:
                target_activities = [main_target_activity] + other_activities
                rules = get_decision_mining_rules_given_activities(log, target_activities, parameters=parameters)
        for n in gateway_map[gw]["edges"]:
            if n in rules:
                rules_per_edge[gateway_map[gw]["edges"][n]["edge"]] = rules[n]
    return rules_per_edge


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


def get_decision_mining_rules_given_activities(log, activities, parameters=None):
    """
    Performs rules discovery thanks to decision mining from a log and a list of activities

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
    rules
        Discovered rules leading to activities
    """
    clf, feature_names, classes, len_list_logs = perform_decision_mining_given_activities(
        log, activities, parameters=parameters)
    rules = get_rules_for_classes(clf, feature_names, classes, len_list_logs)

    return rules


def perform_decision_mining_given_activities(log, activities, parameters=None):
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
    clf
        Decision tree
    feature_names
        Feature names
    classes
        Classes
    len_list_logs
        Length of each sublog considered
    """
    if parameters is None:
        parameters = {}

    max_diff_targets = parameters["max_diff_targets"] if "max_diff_targets" in parameters else 9999999999

    list_logs, considered_activities = log_transforming.get_log_traces_to_activities(log, activities,
                                                                                     parameters=parameters)

    classes = considered_activities
    target = []
    for i in range(len(list_logs)):
        target = target + [min(i, max_diff_targets)] * len(list_logs[i])

    transf_log = EventLog(list(itertools.chain.from_iterable(list_logs)))

    data, feature_names = get_log_representation.get_default_representation(transf_log)

    clf = mine_decision_tree.mine(data, target, max_depth=DEFAULT_MAX_REC_DEPTH_DEC_MINING)

    len_list_logs = [len(x) for x in list_logs]

    return clf, feature_names, classes, len_list_logs


def get_rules_for_classes(tree, feature_names, classes, len_list_logs, rec_depth=0, curr_node=0, rules=None,
                          curr_rec_rule=None):
    """
    Gets the rules that permits to go to a specific class

    Parameters
    -------------
    tree
        Decision tree
    feature_names
        Feature names for the decision tree
    classes
        Classes for the decision tree
    len_list_logs
        Length of each sublog
    rec_depth
        Recursion depth
    curr_node
        Node to consider in the decision tree
    rules
        Already established rules by the recursion algorithm
    curr_rec_rule
        Rule that the current recursion would like to add

    Returns
    -------------
    rules
        Rules that permits to go to each activity
    """
    if rules is None:
        rules = {}
    if curr_rec_rule is None:
        curr_rec_rule = []
    if rec_depth == 0:
        len_list_logs = [1.0 / (1.0 + np.log(x + 1)) for x in len_list_logs]
    feature = tree.tree_.feature[curr_node]
    feature_name = feature_names[feature]
    threshold = tree.tree_.threshold[curr_node]
    child_left = tree.tree_.children_left[curr_node]
    child_right = tree.tree_.children_right[curr_node]
    value = [a * b for a, b in zip(tree.tree_.value[curr_node][0], len_list_logs)]

    if child_left == child_right:
        target_class = classes[np.argmax(value)]
        if curr_rec_rule:
            if target_class not in rules:
                rules[target_class] = []
            rule_to_save = "(" + " && ".join(curr_rec_rule) + ")"
            rules[target_class].append(rule_to_save)
    else:
        if not child_left == curr_node and child_left >= 0:
            new_curr_rec_rule = form_new_curr_rec_rule(curr_rec_rule, False, feature_name, threshold)
            rules = get_rules_for_classes(tree, feature_names, classes, len_list_logs, rec_depth=rec_depth + 1,
                                          curr_node=child_left, rules=rules, curr_rec_rule=new_curr_rec_rule)
        if not child_right == curr_node and child_right >= 0:
            new_curr_rec_rule = form_new_curr_rec_rule(curr_rec_rule, True, feature_name, threshold)
            rules = get_rules_for_classes(tree, feature_names, classes, len_list_logs, rec_depth=rec_depth + 1,
                                          curr_node=child_right, rules=rules, curr_rec_rule=new_curr_rec_rule)
    if rec_depth == 0:
        for act in rules:
            rules[act] = " || ".join(rules[act])
    return rules


def form_new_curr_rec_rule(curr_rec_rule, positive, feature_name, threshold):
    """
    Adds a piece to the recursion rule we would like to add

    Parameters
    -------------
    curr_rec_rule
        Rule that the current recursion would like to add
    positive
        Indicate if we are going left/right in the tree
    feature_name
        Feature name of the current node
    threshold
        Threshold that leads to the current node

    Returns
    ------------
    new_rules
        Updated rules
    """
    new_rules = deepcopy(curr_rec_rule)

    if positive:
        if threshold == 0.5:
            new_rules.append(feature_name.replace("@", " == "))
        else:
            new_rules.append(feature_name + " <= " + str(threshold))
    else:
        if threshold == 0.5:
            new_rules.append(feature_name.replace("@", " != "))
        else:
            new_rules.append(feature_name + " > " + str(threshold))
    return new_rules
