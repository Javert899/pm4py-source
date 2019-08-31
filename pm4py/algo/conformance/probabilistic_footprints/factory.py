import pandas as pd
from pm4py.objects.conversion.log import factory as log_conv_factory
from pm4py.algo.simulation.playout import factory as playout_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory
from pm4py.algo.conformance.probabilistic_footprints.versions import classic_pandas

NO_CASES = "no_cases"
MAX_LEN_TRACE = "max_len_trace"
DEFAULT_NO_CASES = 100
DEFAULT_MAX_LEN_TRACE = 1000

CLASSIC_PANDAS = "classic_pandas"

VERSIONS = {CLASSIC_PANDAS: classic_pandas.apply}

def apply(log, net, im, fm, variant=CLASSIC_PANDAS, parameters=None):
    if parameters is None:
        parameters = {}

    no_cases = parameters[NO_CASES] if NO_CASES in parameters else DEFAULT_NO_CASES
    max_len_trace = parameters[MAX_LEN_TRACE] if MAX_LEN_TRACE in parameters else DEFAULT_MAX_LEN_TRACE

    if not type(log) is pd.DataFrame:
        log = log_conv_factory.apply(log, parameters=log_conv_factory.TO_DATAFRAME)

    playout_traces = playout_factory.apply(net, im,
                                           parameters={"noTraces": no_cases, "maxTraceLength": max_len_trace})

    dfg = dfg_factory.apply(playout_traces)

    return VERSIONS[variant](log, dfg)
