import itertools
import traceback
from copy import deepcopy

import numpy as np
from sklearn import tree

from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.objects.bpmn.util import gateway_map as gwmap_builder
from pm4py.objects.bpmn.util import log_matching
from pm4py.objects.log.log import EventLog
from pm4py.objects.log.util import get_log_representation, get_prefixes
import logging
import json

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
    if parameters is None:
        parameters = {}

    consider_all_elements_to_be_task = parameters[
        "consider_all_elements_to_be_task"] if "consider_all_elements_to_be_task" in parameters else False
    avoid_matching = parameters["avoid_matching"] if "avoid_matching" in parameters else True
    use_node_id = parameters["use_node_id"] if "use_node_id" in parameters else False
    relax_condition_one_entry = parameters[
        "relax_condition_one_entry"] if "relax_condition_one_entry" in parameters else True

    logging.basicConfig(level=logging.INFO)
    logging.info("started get_anchors_from_log_and_bpmn_graph method len(log)=" + str(
        len(log)) + " consider_all_elements_to_be_task=" + str(
        consider_all_elements_to_be_task) + " avoid_matching=" + str(avoid_matching) + " use_node_id=" + str(
        use_node_id) + " relax_condition_one_entry=" + str(relax_condition_one_entry))

    gateway_map, edges_map = gwmap_builder.get_gateway_map(bpmn_graph,
                                                           consider_all_elements_to_be_task=consider_all_elements_to_be_task,
                                                           use_node_id=use_node_id,
                                                           relax_condition_one_entry=relax_condition_one_entry)

    logging.info("len(gateway_map)=" + str(len(gateway_map)) + " len(edges_map)=" + str(len(edges_map)))

    if avoid_matching:
        logging.info("avoid_matching")
        return get_rules_per_edge(log, gateway_map, parameters=parameters)

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
                try:
                    gmgwk = gateway_map[gw]["edges"].keys()
                    for key in gmgwk:
                        if not key == model_to_log[key]:
                            gateway_map[gw]["edges"][n][model_to_log[key]] = gateway_map[gw]["edges"][n][key]
                            del gateway_map[gw]["edges"][n][key]
                except:
                    logging.info("get_rules_per_edge_given_bpmn_and_gw_map EXCEPTION ONE")
                    if gw in gateway_map:
                        del gateway_map[gw]
        except:
            logging.info("get_rules_per_edge_given_bpmn_and_gw_map EXCEPTION TWO")
            # traceback.print_exc()
            del gateway_map[gw]

    logging.info("get_rules_per_edge_given_bpmn_and_gw_map len(gateway_map)+" + str(len(gateway_map)))

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
    if parameters is None:
        parameters = {}

    rules_per_edge = {}
    for gw in gateway_map:
        try:
            rules = None
            rules = {}
            source_activity = gateway_map[gw]["source"]
            if gateway_map[gw]["type"] == "onlytasks":
                target_activities = [x for x in gateway_map[gw]["edges"]]
                logging.info("get_rules_per_edge FIRST " + str(target_activities))
                rules = get_decision_mining_rules_given_activities(log, target_activities, parameters=parameters)
                logging.info("get_rules_per_edge AFTER_FIRST " + str(rules))
            else:
                main_target_activity = list(gateway_map[gw]["edges"].keys())[0]
                logging.info("get_rules_per_edge SECOND0 " + str(main_target_activity))
                other_activities = get_other_activities_connected_to_source(log, source_activity, main_target_activity)
                logging.info("get_rules_per_edge SECOND " + str(other_activities))
                if other_activities:
                    target_activities = [main_target_activity] + other_activities
                    rules = get_decision_mining_rules_given_activities(log, target_activities, parameters=parameters)
                    logging.info("get_rules_per_edge SECOND RULES CALCULATED")
                logging.info("get_rules_per_edge AFTER_SECOND " + str(rules))
            for n in gateway_map[gw]["edges"]:
                if n in rules:
                    logging.info("n in rules = " + str(n))
                    rules_per_edge[gateway_map[gw]["edges"][n]["edge"]] = rules[n]
        except:
            # traceback.print_exc()
            logging.info("exception get_rules_per_edge gw=" + str(gw) + " exception=" + str(traceback.format_exc()))
            pass
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
    logging.info("get_decision_mining_rules_given_activities 0")
    clf, feature_names, classes, len_list_logs = perform_decision_mining_given_activities(
        log, activities, parameters=parameters)
    logging.info(
        "get_decision_mining_rules_given_activities 1 classes=" + str(classes) + " len_list_logs=" + str(len_list_logs))
    rules, correctly_classified, incorrectly_classified = get_rules_for_classes(clf, feature_names, classes,
                                                                                len_list_logs)
    logging.info("get_decision_mining_rules_given_activities 2 rules=" + str(rules))

    ret_rules = {}

    for cl in rules:
        this_precision = float(correctly_classified[cl]) / float(correctly_classified[cl] + incorrectly_classified[cl])
        dectree_overall_precision = float(correctly_classified["@@ALL##"]) / float(
            correctly_classified["@@ALL##"] + incorrectly_classified["@@ALL##"])
        ret_rules[cl] = {"decisionRule": rules[cl], "thisCorrectlyClassified": correctly_classified[cl],
                         "thisIncorrectlyClassified": incorrectly_classified[cl],
                         "thisConsideredItems": correctly_classified[cl] + incorrectly_classified[cl],
                         "allCorrectlyClassified": correctly_classified["@@ALL##"],
                         "allIncorrectlyClassified": incorrectly_classified["@@ALL##"],
                         "allConsideredItems": correctly_classified["@@ALL##"] + incorrectly_classified["@@ALL##"],
                         "thisPrecision": this_precision, "decTreeOverallPrecision": dectree_overall_precision}

    logging.info("get_decision_mining_rules_given_activities 3 ret_rules=" + str(ret_rules))

    return ret_rules


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
    str_tr_attr = parameters["str_tr_attr"] if "str_tr_attr" in parameters else None
    str_ev_attr = parameters["str_ev_attr"] if "str_ev_attr" in parameters else None
    num_tr_attr = parameters["num_tr_attr"] if "num_tr_attr" in parameters else None
    num_ev_attr = parameters["num_ev_attr"] if "num_ev_attr" in parameters else None
    str_evsucc_attr = parameters["str_evsucc_attr"] if "str_evsucc_attr" in parameters else None
    enable_succattr = parameters["enable_succattr"] if "enable_succattr" in parameters else False
    activity_def_representation = parameters[
        "activity_def_representation"] if "activity_def_representation" in parameters else True
    max_rec_depth = parameters["max_rec_depth"] if "max_rec_depth" in parameters else DEFAULT_MAX_REC_DEPTH_DEC_MINING

    list_logs, considered_activities = get_prefixes.get_log_traces_to_activities(log, activities,
                                                                                 parameters=parameters)

    classes = considered_activities
    target = []
    for i in range(len(list_logs)):
        target = target + [min(i, max_diff_targets)] * len(list_logs[i])

    transf_log = EventLog(list(itertools.chain.from_iterable(list_logs)))

    if str_tr_attr is not None or str_ev_attr is not None or num_tr_attr is not None or num_ev_attr is not None or str_evsucc_attr is not None:
        if str_tr_attr is None:
            str_tr_attr = []
        if str_ev_attr is None:
            str_ev_attr = []
        if num_tr_attr is None:
            num_tr_attr = []
        if num_ev_attr is None:
            num_ev_attr = []
        data, feature_names = get_log_representation.get_representation(log, str_tr_attr, str_ev_attr, num_tr_attr,
                                                                        num_ev_attr, str_evsucc_attr=str_evsucc_attr)
    else:
        parameters2 = deepcopy(parameters)
        parameters2[get_log_representation.ENABLE_SUCC_DEF_REPRESENTATION] = enable_succattr
        parameters2[get_log_representation.ENABLE_ACTIVITY_DEF_REPRESENTATION] = activity_def_representation
        data, feature_names = get_log_representation.get_default_representation(transf_log, parameters=parameters2)

    clf = tree.DecisionTreeClassifier(max_depth=max_rec_depth)
    clf.fit(data, target)

    len_list_logs = [len(x) for x in list_logs]

    return clf, feature_names, classes, len_list_logs


def get_rules_for_classes(tree, feature_names, classes, len_list_logs, rec_depth=0, curr_node=0, rules=None,
                          curr_rec_rule=None, correctly_classified=None, incorrectly_classified=None, parameters=None):
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
    parameters
        Parameters of the algorithm

    Returns
    -------------
    rules
        Rules that permits to go to each activity
    """
    if rules is None:
        rules = {}
    if correctly_classified is None:
        correctly_classified = {}
    if incorrectly_classified is None:
        incorrectly_classified = {}
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
        this_correct = tree.tree_.value[curr_node][0][np.argmax(value)]
        this_incorrect = np.sum(
            tree.tree_.value[curr_node][0][idx] for idx in range(len(value)) if not idx == np.argmax(value))
        if curr_rec_rule:
            if target_class not in rules:
                rules[target_class] = []
            if target_class not in correctly_classified:
                correctly_classified[target_class] = 0
            if target_class not in incorrectly_classified:
                incorrectly_classified[target_class] = 0
            if "@@ALL##" not in correctly_classified:
                correctly_classified["@@ALL##"] = 0
            if "@@ALL##" not in incorrectly_classified:
                incorrectly_classified["@@ALL##"] = 0
            correctly_classified[target_class] = correctly_classified[target_class] + this_correct
            incorrectly_classified[target_class] = incorrectly_classified[target_class] + this_incorrect
            correctly_classified["@@ALL##"] = correctly_classified["@@ALL##"] + this_correct
            incorrectly_classified["@@ALL##"] = incorrectly_classified["@@ALL##"] + this_incorrect

            rule_to_save = "(" + " && ".join(curr_rec_rule) + ")"
            rules[target_class].append(rule_to_save)
    else:
        if not child_left == curr_node and child_left >= 0:
            new_curr_rec_rule = form_new_curr_rec_rule(curr_rec_rule, False, feature_name, threshold)
            rules, correctly_classified, incorrectly_classified = get_rules_for_classes(tree, feature_names, classes,
                                                                                        len_list_logs,
                                                                                        rec_depth=rec_depth + 1,
                                                                                        curr_node=child_left,
                                                                                        rules=rules,
                                                                                        curr_rec_rule=new_curr_rec_rule,
                                                                                        correctly_classified=correctly_classified,
                                                                                        incorrectly_classified=incorrectly_classified,
                                                                                        parameters=parameters)
        if not child_right == curr_node and child_right >= 0:
            new_curr_rec_rule = form_new_curr_rec_rule(curr_rec_rule, True, feature_name, threshold)
            rules, correctly_classified, incorrectly_classified = get_rules_for_classes(tree, feature_names, classes,
                                                                                        len_list_logs,
                                                                                        rec_depth=rec_depth + 1,
                                                                                        curr_node=child_right,
                                                                                        rules=rules,
                                                                                        curr_rec_rule=new_curr_rec_rule,
                                                                                        correctly_classified=correctly_classified,
                                                                                        incorrectly_classified=incorrectly_classified,
                                                                                        parameters=parameters)
    if rec_depth == 0:
        for act in rules:
            rules[act] = " || ".join(rules[act])
    return rules, correctly_classified, incorrectly_classified


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
        if threshold == 0.5 and "@" in feature_name:
            new_rules.append(feature_name.replace("@", " == "))
        else:
            new_rules.append(feature_name + " > " + str(threshold))
    else:
        if threshold == 0.5 and "@" in feature_name:
            new_rules.append(feature_name.replace("@", " != "))
        else:
            new_rules.append(feature_name + " <= " + str(threshold))
    return new_rules
