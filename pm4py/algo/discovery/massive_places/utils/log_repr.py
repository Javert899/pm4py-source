from pm4py.objects.log.util import xes
from pm4py.statistics.traces.log.case_statistics import get_variant_statistics
from pm4py.util import constants
from pm4py.algo.filtering.log.attributes import attributes_filter
from copy import copy
import numpy as np


def get_log_repr(log, parameters):
    if parameters is None:
        parameters = {}

    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY

    var_stats = get_variant_statistics(log, parameters=parameters)

    compl_var_repr = []
    par_var_repr = []
    sum_variants = 0
    feature_names = list(attributes_filter.get_attribute_values(log, activity_key).keys())

    for var in var_stats:
        variant = var["variant"].split(",")
        count = var["count"]

        this_var_repr = [0] * len(feature_names)

        for act in variant:
            i = feature_names.index(act)
            this_var_repr[i] = this_var_repr[i] + count
            compl_var_repr.append(copy(this_var_repr))
            sum_variants = sum_variants + count

        par_var_repr.append(this_var_repr)

    compl_var_repr = np.asmatrix(compl_var_repr)
    par_var_repr = np.asmatrix(par_var_repr)

    compl_var_repr = np.unique(compl_var_repr, axis=0)
    par_var_repr = np.unique(par_var_repr, axis=0)

    return compl_var_repr, par_var_repr, sum_variants, feature_names
