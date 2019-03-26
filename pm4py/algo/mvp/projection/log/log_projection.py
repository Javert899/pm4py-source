from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.attributes import attributes_filter
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.algo.mvp.utils import df_to_grouped_stream
from pm4py.objects.log.log import EventLog, Trace, Event
from pm4py.objects.log.util import sorting

ENABLE_ENDPOINTS_FILTER = "enable_endpoints_filter"
START_ACTIVITIES = "start_activities"
END_ACTIVITIES = "end_activities"
ENABLE_ACTIVITIES_FILTER = "enable_activities_filter"
ACTIVITIES = "activities"
ENABLE_VARIANTS_FILTER = "enable_variants_filter"

DECREASING_FACTOR = "decreasingFactor"
DEFAULT_DECR_FACTOR = 0.1


def apply(df, perspectives_list, parameters=None):
    """
    Apply the projection from a dataframe to a log object

    Parameters
    -------------
    df
        Dataframe
    perspectives_list
        Perspectives list

    Returns
    -------------
    log
        Event log
    """
    if parameters is None:
        parameters = {}

    enable_endpoints_filter = parameters[ENABLE_ENDPOINTS_FILTER] if ENABLE_ENDPOINTS_FILTER in parameters else False
    start_activities = parameters[START_ACTIVITIES] if START_ACTIVITIES in parameters else dict()
    end_activities = parameters[END_ACTIVITIES] if END_ACTIVITIES in parameters else dict()

    enable_activities_filter = parameters[ENABLE_ACTIVITIES_FILTER] if ENABLE_ACTIVITIES_FILTER in parameters else False
    activities = parameters[ACTIVITIES] if ACTIVITIES in parameters else list()

    enable_variants_filter = parameters[ENABLE_VARIANTS_FILTER] if ENABLE_VARIANTS_FILTER in parameters else False

    if "decreasingFactor" not in parameters:
        parameters["decreasingFactor"] = DEFAULT_DECR_FACTOR

    trace_by_persp_value = {}
    for p in perspectives_list:
        trace_by_persp_value[p] = {}
    grouped_stream = df_to_grouped_stream.apply(df, remove_common=True, include_activity_timest_in_key=True)
    for event in grouped_stream:
        key_value = {k: v for x in grouped_stream[event] for k, v in x.items()}
        keys_set = set(key_value.keys())
        perspectives_to_consider = keys_set.intersection(perspectives_list)
        if perspectives_to_consider:
            existing_traces = {}
            existing_traces_set = set()
            for p in perspectives_to_consider:
                v = key_value[p]
                if v in trace_by_persp_value[p]:
                    existing_traces[p] = v
                    existing_traces_set.add(trace_by_persp_value[p][v])

            if len(existing_traces_set) == 0:
                new_trace = Trace()
            elif len(existing_traces_set) == 1:
                new_trace = list(existing_traces_set)[0]
            else:
                new_trace = Trace()
                for trace in existing_traces_set:
                    for eve in trace:
                        if eve not in new_trace:
                            new_trace.append(eve)
            xes_event = Event()
            xes_event["event_id"] = event[0]
            xes_event["concept:name"] = event[1]
            xes_event["time:timestamp"] = event[2]

            new_trace.append(xes_event)

            for p in perspectives_to_consider:
                v = key_value[p]
                xes_event[p] = v
            for p in perspectives_to_consider:
                v = key_value[p]
                trace_by_persp_value[p][v] = new_trace
    log = EventLog()
    for p in trace_by_persp_value:
        for v in trace_by_persp_value[p]:
            t = trace_by_persp_value[p][v]
            if t not in log:
                log.append(t)

    log = sorting.sort_timestamp(log)

    if enable_endpoints_filter:
        log = start_activities_filter.apply(log, start_activities)
        log = end_activities_filter.apply(log, end_activities)
    if enable_activities_filter:
        log = attributes_filter.apply_events(log, activities)
    if enable_variants_filter:
        log = variants_filter.apply_auto_filter(log, parameters=parameters)

    # filter empty traces
    log = EventLog([trace for trace in log if len(trace) > 0])

    return log


def get_perspective_filt_log_from_df_and_mvp_and_perspective(df, mvp, p, parameters=None):
    """
    Gets a log from a perspective, that is already filtered

    Parameters
    -------------
    df
        Dataframe
    mvp
        Multiple Viewpoint model
    p
        Perspective
    parameters
        Parameters of the algorithm

    Returns
    -------------
    log
        Filtered event log
    """
    if parameters is None:
        parameters = {}

    start_activities = list(mvp[p].start_activities[0].keys())
    end_activities = list(mvp[p].end_activities[0].keys())
    activities = list(mvp[p].nodes.keys())
    parameters[ENABLE_ENDPOINTS_FILTER] = True
    parameters[ENABLE_ACTIVITIES_FILTER] = True
    parameters[ENABLE_VARIANTS_FILTER] = True

    if START_ACTIVITIES not in parameters:
        parameters[START_ACTIVITIES] = start_activities
    if END_ACTIVITIES not in parameters:
        parameters[END_ACTIVITIES] = end_activities
    if ACTIVITIES not in parameters:
        parameters[ACTIVITIES] = activities

    log = apply(df, [p], parameters=parameters)

    return log
