from pm4py.algo.starstar.utils import df_to_grouped_stream
from pm4py.objects.log.log import EventLog, Trace, Event
from pm4py.objects.log.util import sorting


def apply(df, perspectives_list):
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
    trace_by_persp_value = {}
    for p in perspectives_list:
        trace_by_persp_value[p] = {}
    grouped_stream = df_to_grouped_stream.apply(df, remove_common=True, include_activity_timest_in_key=True)
    for event in grouped_stream:
        key_value = {k:v for x in grouped_stream[event] for k,v in x.items()}
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

    return log
