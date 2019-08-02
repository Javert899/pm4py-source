from sklearn.linear_model import ElasticNet

from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.log import EventLog
from pm4py.objects.log.util import get_log_representation
from pm4py.objects.log.util import sorting
from pm4py.objects.log.util import xes
from pm4py.objects.log.util.get_prefixes import get_log_with_log_prefixes
from pm4py.util import constants
from pm4py.util.business_hours import BusinessHours


def get_remaining_time_from_log(log, max_len_trace=100000, parameters=None):
    """
    Gets the remaining time for the instances given a log and a trace index

    Parameters
    ------------
    log
        Log
    max_len_trace
        Index
    parameters
        Parameters of the algorithm

    Returns
    ------------
    list
        List of remaining times
    """
    if parameters is None:
        parameters = {}
    timestamp_key = parameters[
        constants.PARAMETER_CONSTANT_TIMESTAMP_KEY] if constants.PARAMETER_CONSTANT_TIMESTAMP_KEY in parameters else xes.DEFAULT_TIMESTAMP_KEY
    business_hours = parameters["business_hours"] if "business_hours" in parameters else False
    worktiming = parameters["worktiming"] if "worktiming" in parameters else [7, 17]
    weekends = parameters["weekends"] if "weekends" in parameters else [6, 7]
    y_orig = []
    for trace in log:
        y_orig.append([])
        for index, event in enumerate(trace):
            if index >= max_len_trace:
                break
            timestamp_st = trace[index][timestamp_key]
            timestamp_et = trace[-1][timestamp_key]
            if business_hours:
                bh = BusinessHours(timestamp_st.replace(tzinfo=None), timestamp_et.replace(tzinfo=None), worktiming=worktiming, weekends=weekends)
                y_orig[-1].append(bh.getseconds())
            else:
                y_orig[-1].append((timestamp_et - timestamp_st).total_seconds())
        while len(y_orig[-1]) < max_len_trace:
            y_orig[-1].append(y_orig[-1][-1])
    return y_orig


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
    business_hours = parameters["business_hours"] if "business_hours" in parameters else False
    worktiming = parameters["worktiming"] if "worktiming" in parameters else [7, 17]
    weekends = parameters["weekends"] if "weekends" in parameters else [6, 7]

    y_orig = parameters["y_orig"] if "y_orig" in parameters else None

    log = sorting.sort_timestamp(log, timestamp_key)

    str_evsucc_attr = [activity_key]
    if "str_ev_attr" in parameters:
        str_tr_attr = parameters["str_tr_attr"] if "str_tr_attr" in parameters else []
        str_ev_attr = parameters["str_ev_attr"] if "str_ev_attr" in parameters else []
        num_tr_attr = parameters["num_tr_attr"] if "num_tr_attr" in parameters else []
        num_ev_attr = parameters["num_ev_attr"] if "num_ev_attr" in parameters else []
    else:
        str_tr_attr, str_ev_attr, num_tr_attr, num_ev_attr = attributes_filter.select_attributes_from_log_for_tree(log)
        if activity_key not in str_ev_attr:
            str_ev_attr.append(activity_key)

    ext_log, change_indexes = get_log_with_log_prefixes(log)
    data, feature_names = get_log_representation.get_representation(ext_log, str_tr_attr, str_ev_attr, num_tr_attr,
                                                                    num_ev_attr, str_evsucc_attr=str_evsucc_attr)

    if y_orig is not None:
        remaining_time = [y for x in y_orig for y in x]
    else:
        if business_hours:
            remaining_time = []
            for trace in ext_log:
                if trace:
                    timestamp_et = trace[-1][timestamp_key]
                    timestamp_st = trace[0][timestamp_key]

                    bh = BusinessHours(timestamp_st.replace(tzinfo=None), timestamp_et.replace(tzinfo=None),
                                       worktiming=worktiming, weekends=weekends)
                    remaining_time.append(bh.getseconds())
                else:
                    remaining_time.append(0)
        else:
            remaining_time = []
            for trace in ext_log:
                if trace:
                    remaining_time.append((trace[-1][timestamp_key] - trace[0][timestamp_key]).total_seconds())
                else:
                    remaining_time.append(0)
    regr = ElasticNet(max_iter=10000, l1_ratio=0.7)
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
