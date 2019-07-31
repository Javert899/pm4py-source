from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.pandas.start_activities import start_activities_filter
from pm4py.algo.filtering.pandas.end_activities import end_activities_filter
from pm4py.algo.mvp.crd import mine_producer, mine_consumer
from pm4py.util import constants
from pm4py.objects.heuristics_net import defaults

MIN_ACT_COUNT = "min_act_count"
MIN_DFG_OCCURRENCES = "min_dfg_occurrences"


def apply(df, parameters=None):
    if parameters is None:
        parameters = {}

    min_act_count = parameters[MIN_ACT_COUNT] if MIN_ACT_COUNT in parameters else defaults.DEFAULT_MIN_ACT_COUNT
    min_dfg_occurrences = parameters[
        MIN_DFG_OCCURRENCES] if MIN_DFG_OCCURRENCES in parameters else defaults.DEFAULT_MIN_DFG_OCCURRENCES
    min_acti_count_in_perspective = parameters[
        defaults.MIN_ACTI_COUNT_IN_PERSPECTIVE] if defaults.MIN_ACTI_COUNT_IN_PERSPECTIVE in parameters else defaults.DEFAULT_MIN_ACTI_COUNT_IN_PERSPECTIVE


    consumers = mine_consumer.mine_consumer(df)
    producers = mine_producer.mine_producer(df)


    ret = {}

    columns = sorted(list(df.columns))

    for col in columns:

        if not col.startswith("event_"):
            red_df = df[["event_id", "event_activity", "event_timestamp", col]]
            red_df = red_df.groupby(["event_id", "event_activity", col]).first().reset_index()

            dfg = df_statistics.get_dfg_graph(red_df, sort_timestamp_along_case_id=True, sort_caseid_required=True,
                                              activity_key="event_activity", timestamp_key="event_timestamp",
                                              case_id_glue=col)

            activities_count = attributes_filter.get_attribute_values(red_df, "event_activity")
            activities_count = {x: y for x, y in activities_count.items() if y >= min_act_count}

            if len(activities_count) >= min_acti_count_in_perspective:
                start_activities = start_activities_filter.get_start_activities(red_df, parameters={
                    constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "event_activity",
                    constants.PARAMETER_CONSTANT_CASEID_KEY: "event_timestamp"})

                end_activities = end_activities_filter.get_end_activities(red_df, parameters={
                    constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "event_activity",
                    constants.PARAMETER_CONSTANT_CASEID_KEY: "event_timestamp"})

                dfg = {x: y for x, y in dfg.items() if
                       x[0] in activities_count and x[1] in activities_count and y >= min_dfg_occurrences}

                if len(activities_count) > 0:
                    ret[col] = {}
                    ret[col]["dfg"] = dfg
                    ret[col]["activities_count"] = activities_count
                    ret[col]["start_activities"] = start_activities
                    ret[col]["end_activities"] = end_activities

    ret["@@producers"] = producers
    ret["@@consumers"] = consumers

    return ret
