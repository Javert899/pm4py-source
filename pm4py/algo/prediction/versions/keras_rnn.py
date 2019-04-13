import math
from copy import deepcopy

import numpy as np
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.models import Sequential

from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.objects.log.log import EventLog
from pm4py.objects.log.util import get_log_representation
from pm4py.objects.log.util import xes
from pm4py.util import constants


def get_trace_rep_rnn(trace, dictionary_features, max_len_trace):
    """
    Gets a trace representation for RNN training

    Parameters
    ------------
    trace
        Trace
    dictionary_features
        Ordered dictionary of features
    max_len_trace
        Maximum length of the trace in the log

    Returns
    ------------
    X
        double list that contains the value for each feature for each event of the trace
    """
    X = []
    for index in range(min(len(trace), max_len_trace)):
        event = trace[index]
        ev_vector = [0] * len(dictionary_features)
        for attribute_name in event:
            attribute_value = event[attribute_name]
            rep = "event:" + str(attribute_name) + "@" + str(attribute_value)
            if rep in dictionary_features:
                ev_vector[dictionary_features[rep]] = 1
        if index < len(trace) - 1:
            next_event = trace[index + 1]
            for attribute_name in event:
                if attribute_name in next_event:
                    attribute_value_1 = event[attribute_name]
                    attribute_value_2 = next_event[attribute_name]
                    rep = "succession:" + str(attribute_name) + "@" + str(attribute_value_1) + "#" + str(
                        attribute_value_2)
                    if rep in dictionary_features:
                        ev_vector[dictionary_features[rep]] = 1
        X.append(ev_vector)
    j = len(trace)
    while j < max_len_trace:
        # print(X[-1])
        X.append(np.zeros(len(X[-1])))
        j = j + 1
    X = np.transpose(np.asmatrix(X))
    X = X.tolist()

    return X


def get_log_rep_rnn(log, dictionary_features, max_len_trace):
    """
    Gets a log representation for RNN training

    Parameters
    -------------
    log
        Log
    dictionary_features
        Ordered dictionary of features
    max_len_trace
        Maximum length of the trace in the log

    Returns
    -------------
    X
        triple list that describes the log
    """
    X = []
    for trace in log:
        rep = get_trace_rep_rnn(trace, dictionary_features, max_len_trace)
        if rep:
            X.append(rep)

    return X


def get_X_from_log(log, feature_names, max_len_trace):
    """
    Gets the eventual X matrix for a given log

    Parameters
    -------------
    log
        Log
    feature_names
        List of features contained in the log
    max_len_trace
        Maximum length of the trace in the log

    Returns
    -------------
    X
        3D matrix that describes the log
    """
    dictionary_features = {}
    for index, value in enumerate(feature_names):
        dictionary_features[value] = index
    X = get_log_rep_rnn(log, dictionary_features, max_len_trace)
    X = np.array(X)

    return X


def group_remaining_time(change_indexes, remaining_time, max_len_trace):
    """
    Groups the remaining time of the extended log according to the change indexes

    Parameters
    -------------
    change_indexes
        Change indexes between cases in the extended log
    remaining_time
        List of the remaining times
    max_len_trace
        Maximum length of the trace in the log

    Returns
    -------------
    rem_time_grouped
        Remaining time grouped by case
    """
    rem_time_grouped = []
    j = 0
    for ct in change_indexes:
        rem = []
        added = False

        for i in range(len(ct)):
            rem.append(remaining_time[j])
            if i == max_len_trace - 1:
                rem_time_grouped.append(deepcopy(rem))
                added = True
            elif i == len(ct) - 1 and not added:
                while len(rem) < max_len_trace:
                    rem.append(rem[-1])
                rem_time_grouped.append(deepcopy(rem))
            j = j + 1
    return rem_time_grouped


def normalize_remaining_time(rem_time_grouped):
    """
    Normalize the remaining time using logarithmic function

    Parameters
    -------------
    rem_time_grouped
        Remaining time grouped by case

    Returns
    -------------
    normalized_rem_time
        Normalized remaining time
    """
    ret = []
    max_value = -10000000
    for lst in rem_time_grouped:
        max_lst = max(lst)
        max_value = max(max_value, max_lst)
    log_max_value = math.log(1.0 + max_value)
    for lst in rem_time_grouped:
        ret.append([])
        for val in lst:
            ret[-1].append(-1.0 + 2.0 * (math.log(val + 1.0) / log_max_value))
    return ret, log_max_value


def reconstruct_value(y, log_max_value):
    """
    Reconstruct the value to return in test phase

    Parameters
    -------------
    y
        Logarithmic value predicted by the algorithm
    log_max_value
        Logarithm of the maximum value

    Returns
    -------------
    rec_value
        Reconstructed value
    """
    if y < -1:
        y = -1
    return math.exp((y + 1.0) / 2.0 * log_max_value) - 1


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
    y_orig = []
    for trace in log:
        y_orig.append([])
        for index, event in enumerate(trace):
            if index >= max_len_trace:
                break
            y_orig[-1].append((trace[-1][timestamp_key] - trace[index][timestamp_key]).total_seconds())
        while len(y_orig[-1]) < max_len_trace:
            y_orig[-1].append(y_orig[-1][-1])
    return y_orig


def train(log, parameters=None):
    """
    Train the model

    Parameters
    -------------
    log
        Log
    parameters
        Possible parameters of the algorithm, including default_epochs
    """
    if parameters is None:
        parameters = {}
    default_epochs = parameters["default_epochs"] if "default_epochs" in parameters else 50
    parameters["enable_sort"] = False
    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    # log = sorting.sort_timestamp(log, timestamp_key)
    max_len_trace = max([len(trace) for trace in log])
    y_orig = parameters["y_orig"] if "y_orig" in parameters else get_remaining_time_from_log(log,
                                                                                             max_len_trace=max_len_trace,
                                                                                             parameters=parameters)
    y, log_max_value = normalize_remaining_time(y_orig)
    y = np.array(y)
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

    data, feature_names = get_log_representation.get_representation(log, str_tr_attr, str_ev_attr, num_tr_attr,
                                                                    num_ev_attr, str_evsucc_attr=str_evsucc_attr)
    X = get_X_from_log(log, feature_names, max_len_trace)
    in_out_neurons = X.shape[2]
    hidden_neurons = min(int(in_out_neurons * 7.5), 50)
    input_shape = (X.shape[1], X.shape[2])
    model = Sequential()
    model.add(LSTM(hidden_neurons, return_sequences=False, input_shape=input_shape))
    model.add(Dense(in_out_neurons))
    model.add(Activation("linear"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop")
    model.fit(X, y, batch_size=X.shape[1], nb_epoch=default_epochs, validation_split=0.2)
    return {"str_tr_attr": str_tr_attr, "str_ev_attr": str_ev_attr, "num_tr_attr": num_tr_attr,
            "num_ev_attr": num_ev_attr, "str_evsucc_attr": str_evsucc_attr, "feature_names": feature_names,
            "regr": model, "max_len_trace": max_len_trace,
            "log_max_value": log_max_value, "variant": "keras_rnn"}


def test(model, obj, parameters=None):
    """
    Test the model

    Parameters
    -------------
    model
        Model obtained by Keras
    obj
        Object to test (log/trace)
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    pred
        Result of the prediction (single value / list)
    """
    if parameters is None:
        parameters = {}
    feature_names = model["feature_names"]
    regr = model["regr"]
    max_len_trace = model["max_len_trace"]
    log_max_value = model["log_max_value"]
    if type(obj) is EventLog:
        log = obj
    else:
        log = EventLog([obj])
    X = get_X_from_log(log, feature_names, max_len_trace)
    y = regr.predict(X)
    if len(log) == 1:
        return reconstruct_value(y[0][len(log[0]) - 1], log_max_value)
    else:
        ret = []
        for index, trace in enumerate(log):
            ret.append(reconstruct_value(y[index][len(trace) - 1], log_max_value))
        return ret
