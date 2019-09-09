from pm4py.algo.mvp.utils import df_to_grouped_stream_old


def apply(df, remove_common=False, include_activity_timest_in_key=False):
    """
    Dataframe to grouped stream

    Parameters
    -------------
    df
        Dataframe

    Returns
    -------------
    grouped_stream
        Grouped stream of events
    """

    grouped_stream = df_to_grouped_stream_old.apply(df, remove_common=remove_common,
                                                    include_activity_timest_in_key=include_activity_timest_in_key)

    ret = []

    for gk in grouped_stream:
        g = grouped_stream[gk]
        if g:
            ev = {}
            keys = set()
            for i in range(len(g)):
                keys = keys.union(set(g[i].keys()))
            for key in keys:
                if key.startswith("event_"):
                    ev[key] = g[0][key]
                else:
                    ev[key] = [g[i][key] for i in range(len(g)) if key in g[i]]
            ret.append(ev)

    return ret
