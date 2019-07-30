from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.pandas.start_activities import start_activities_filter
from pm4py.algo.filtering.pandas.end_activities import end_activities_filter
from pm4py.util import constants


def apply(df, parameters=None):
    if parameters is None:
        parameters = {}

    ret = {}

    columns = sorted(list(df.columns))

    for col in columns:

        if not col.startswith("event_"):
            red_df = df[["event_id", "event_activity", "event_timestamp", col]]
            #print(len(red_df))
            #print(red_df)
            red_df = red_df.groupby(["event_id", "event_activity", col]).first().reset_index()
            #print(len(red_df))
            #print(red_df)
            print(red_df)

            dfg = df_statistics.get_dfg_graph(red_df, sort_timestamp_along_case_id=True, sort_caseid_required=True,
                                              activity_key="event_activity", timestamp_key="event_timestamp",
                                              case_id_glue=col)

            activities_count = attributes_filter.get_attribute_values(red_df, "event_activity")

            start_activities = start_activities_filter.get_start_activities(red_df, parameters={
                constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "event_activity",
                constants.PARAMETER_CONSTANT_CASEID_KEY: "event_timestamp"})

            end_activities = end_activities_filter.get_end_activities(red_df, parameters={
                constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "event_activity",
                constants.PARAMETER_CONSTANT_CASEID_KEY: "event_timestamp"})

            if len(dfg) > 0:
                ret[col] = {}
                ret[col]["dfg"] = dfg
                ret[col]["activities_count"] = activities_count
                ret[col]["start_activities"] = start_activities
                ret[col]["end_activities"] = end_activities

    return ret
