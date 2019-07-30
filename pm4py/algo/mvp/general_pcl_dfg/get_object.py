from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics

def apply(df, parameters=None):
    if parameters is None:
        parameters = {}

    ret = {}

    columns = sorted(list(df.columns))

    for col in columns:


        if not col.startswith("event_"):
            ret[col] = {}

            red_df = df[["event_activity", "event_timestamp", col]].dropna()

            dfg = df_statistics.get_dfg_graph(red_df, sort_timestamp_along_case_id=False, sort_caseid_required=False,
                                               activity_key="event_activity", timestamp_key="event_timestamp", case_id_glue=col)

            ret[col]["dfg"] = dfg

    return ret
