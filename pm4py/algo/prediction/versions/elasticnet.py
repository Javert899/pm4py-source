from sklearn.linear_model import ElasticNet

from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.log import EventLog
from pm4py.objects.log.util import get_log_representation
from pm4py.objects.log.util import sorting
from pm4py.objects.log.util import xes
from pm4py.objects.log.util.get_prefixes import get_log_with_log_prefixes
from pm4py.statistics.traces.log import case_statistics
from pm4py.util import constants


def train(log, parameters=None):
    """
    Train the prediction model

    Parameters
    -----------
    log
        Event log
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    model
        Trained model
    """
    if parameters is None:
        parameters = {}

    parameters["enable_sort"] = False
    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    timestamp_key = parameters[
        constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] if constants.PARAMETER_CONSTANT_TIMESTAMP_KEY in parameters else xes.DEFAULT_TIMESTAMP_KEY

    log = sorting.sort_timestamp(log, timestamp_key)

    str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr = attributes_filter.select_attributes_from_log_for_tree(log)
    if activity_key not in str_ev_attr:
        str_ev_attr.append(activity_key)
    str_evsucc_attr = [activity_key]

    ext_log, change_indexes = get_log_with_log_prefixes(log)
    data, feature_names = get_log_representation.get_representation(ext_log, str_tr_attr, str_ev_attr, num_tr_attr,
                                                                    num_ev_attr, str_evsucc_attr=str_evsucc_attr)
    case_durations = case_statistics.get_all_casedurations(ext_log, parameters=parameters)

    change_indexes_flattened = [y for x in change_indexes for y in x]
    remaining_time = [-case_durations[i] + case_durations[change_indexes_flattened[i]] for i in
                      range(len(case_durations))]

    regr = ElasticNet()
    regr.fit(data, remaining_time)

    return {"str_tr_attr": str_tr_attr, "str_ev_attr": str_ev_attr, "num_tr_attr": num_tr_attr,
            "num_ev_attr": num_ev_attr, "str_evsucc_attr": str_evsucc_attr, "feature_names": feature_names,
            "remaining_time": remaining_time, "regr": regr, "variant": "elasticnet"}


def test(model, obj, parameters=None):
    """
    Test the prediction model

    Parameters
    ------------
    model
        Prediction model
    obj
        Object to predict (Trace / EventLog)
    parameters
        Possible parameters of the algorithm

    Returns
    ------------
    pred
        Result of the prediction (single value / list)
    """
    if parameters is None:
        parameters = {}

    str_tr_attr = model["str_tr_attr"]
    str_ev_attr = model["str_ev_attr"]
    num_tr_attr = model["num_tr_attr"]
    num_ev_attr = model["num_ev_attr"]
    str_evsucc_attr = model["str_evsucc_attr"]
    feature_names = model["feature_names"]
    regr = model["regr"]

    if type(obj) is EventLog:
        log = obj
    else:
        log = EventLog([obj])
    data, feature_names = get_log_representation.get_representation(log, str_tr_attr, str_ev_attr, num_tr_attr,
                                                                    num_ev_attr, str_evsucc_attr=str_evsucc_attr,
                                                                    feature_names=feature_names)
    pred = regr.predict(data)

    if len(pred) == 1:
        # prediction on a single case
        return pred[0]
    else:
        return pred
