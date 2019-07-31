from pm4py.algo.mvp.crd import get_last_for_object
from pm4py.objects.heuristics_net import defaults
import math


def mine_consumer(df, parameters=None):
    if parameters is None:
        parameters = {}

    cols = [x for x in df.columns if not x.startswith("event_")]

    ratio_log_producer = parameters[
        defaults.RATIO_LOG_PRODUCER] if defaults.RATIO_LOG_PRODUCER in parameters else defaults.DEFAULT_RATIO_LOG_PRODUCER
    min_act_count = parameters[
        defaults.MIN_ACT_COUNT] if defaults.MIN_ACT_COUNT in parameters else defaults.DEFAULT_MIN_ACT_COUNT + 1
    min_dfg_occurrences = parameters[
        defaults.MIN_DFG_OCCURRENCES] if defaults.MIN_DFG_OCCURRENCES in parameters else defaults.DEFAULT_MIN_DFG_OCCURRENCES
    min_acti_count_in_perspective = parameters[
        defaults.MIN_ACTI_COUNT_IN_PERSPECTIVE] if defaults.MIN_ACTI_COUNT_IN_PERSPECTIVE in parameters else defaults.DEFAULT_MIN_ACTI_COUNT_IN_PERSPECTIVE

    activities_count_per_class = {}
    consumer_per_class = {}
    relations_per_class = {}

    for iii, col in enumerate(cols):
        red_df = df[["event_id", "event_activity", "event_timestamp", col]].dropna()
        red_df["@@index"] = red_df.index
        red_df = red_df.sort_values([col, "event_timestamp", "@@index"])
        red_df = red_df.drop("@@index", axis=1)
        red_df = red_df.groupby("event_id").last().reset_index()

        if len(red_df) > 0:
            activities_count_per_class[col] = dict(red_df["event_activity"].value_counts())
            all_keys = list(activities_count_per_class[col])
            for key in all_keys:
                if activities_count_per_class[col][key] < min_act_count:
                    del activities_count_per_class[col][key]

            if len(activities_count_per_class[col]) < min_acti_count_in_perspective:
                del activities_count_per_class[col]
            else:
                for jjj, c2 in enumerate(cols):
                    if not col == c2:

                        parameters["target_col"] = c2
                        last_obj_df = get_last_for_object.get_last(df, parameters=parameters).dropna(axis='columns',
                                                                                                     how='all')
                        if len(last_obj_df) > 0 and c2 in last_obj_df.columns:
                            last_obj_df["@@index"] = last_obj_df.index
                            last_obj_df = last_obj_df.sort_values([c2, "event_timestamp", "@@index"])
                            last_obj_df = last_obj_df.drop("@@index", axis=1)

                            print("mine_consumer", iii, len(cols), col, jjj, len(cols), c2)

                            last_obj_df.columns = [x + "_2" for x in last_obj_df.columns]

                            joined_df = red_df.merge(last_obj_df, left_on="event_id", right_on="event_id_2",
                                                     suffixes=('', ''))

                            other_cols = list(
                                x for x in joined_df.columns if
                                x.endswith("_2") and not x.startswith("@@")
                                and not x.startswith("event_") and not x.startswith(col))

                            allowed_cols = ["event_id", "event_activity", col] + other_cols

                            red_joined_df = joined_df[allowed_cols]
                            red_joined_df = red_joined_df.dropna(subset=[col], how="any")
                            red_joined_df = red_joined_df.dropna(axis='columns', how='all')

                            if len(red_joined_df) > 0:
                                if c2 + "_2" in red_joined_df.columns:
                                    if col in activities_count_per_class and c2 in activities_count_per_class:
                                        red_joined_df_group_col = red_joined_df.groupby(col)
                                        red_joined_df_group_c2 = red_joined_df.groupby(c2 + "_2")

                                        if col not in consumer_per_class:
                                            consumer_per_class[col] = {}
                                            relations_per_class[col] = {}
                                        consumer_per_class[col][c2] = dict(red_joined_df["event_activity"].value_counts())
                                        all_keys = list(consumer_per_class[col][c2].keys())
                                        for act in all_keys:
                                            if act in activities_count_per_class[col] and act in activities_count_per_class[
                                                c2]:
                                                amount_c1 = activities_count_per_class[col][act]
                                                amount_c2 = activities_count_per_class[c2][act]

                                                relations_per_class[col][c2] = {}

                                                if len(red_joined_df_group_col) < len(red_joined_df_group_c2):
                                                    if len(red_joined_df_group_c2) < amount_c1 or len(all_keys) > 1:
                                                        if len(red_joined_df_group_c2) < amount_c2 or len(all_keys) > 1:
                                                            relations_per_class[col][c2][act] = ["0..1", "0..N"]
                                                        else:
                                                            relations_per_class[col][c2][act] = ["0..1", "1..N"]
                                                    else:
                                                        if len(red_joined_df_group_c2) < amount_c2:
                                                            relations_per_class[col][c2][act] = ["1..1", "0..N"]
                                                        else:
                                                            relations_per_class[col][c2][act] = ["1..1", "1..N"]
                                                else:
                                                    if len(red_joined_df_group_c2) < amount_c1 or len(all_keys) > 1:
                                                        if len(red_joined_df_group_c2) < amount_c2 or len(all_keys) > 1:
                                                            relations_per_class[col][c2][act] = ["0..1", "0..1"]
                                                        else:
                                                            relations_per_class[col][c2][act] = ["0..1", "1..1"]
                                                    else:
                                                        if len(red_joined_df_group_c2) < amount_c2:
                                                            relations_per_class[col][c2][act] = ["1..1", "0..1"]
                                                        else:
                                                            relations_per_class[col][c2][act] = ["1..1", "1..1"]
                                                this_amount = consumer_per_class[col][c2][act]
                                                c1_ratio = math.log(1.0 + this_amount) / (
                                                        math.log(1.0 + amount_c1) + 0.0000001)
                                                c2_ratio = math.log(1.0 + this_amount) / (
                                                        math.log(1.0 + amount_c2) + 0.0000001)

                                                if (
                                                        c1_ratio < ratio_log_producer and c2_ratio < ratio_log_producer) or this_amount < min_dfg_occurrences:
                                                    del consumer_per_class[col][c2][act]
                                            else:
                                                del consumer_per_class[col][c2][act]

    return {"activities_count_per_class": activities_count_per_class,
            "consumer_per_class": consumer_per_class, "relations_per_class": relations_per_class}
