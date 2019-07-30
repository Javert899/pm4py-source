from pm4py.algo.mvp.crd import get_first_for_object


def mine_producer(df, parameters=None):
    if parameters is None:
        parameters = {}

    cols = [x for x in df.columns if not x.startswith("event_")]

    activities_count_per_class = {}
    producer_per_class = {}

    for col in cols:
        red_df = df[["event_id", "event_activity", col]].dropna().groupby("event_id").first().reset_index()
        activities_count_per_class[col] = dict(red_df["event_activity"].value_counts())

        for c2 in cols:
            if not col == c2:
                parameters["target_col"] = c2
                first_obj_df = get_first_for_object.get_first(df, parameters=parameters).dropna(axis='columns', how='all')
                first_obj_df.columns = [x+"_2" for x in first_obj_df.columns]

                joined_df = red_df.merge(first_obj_df, left_on="event_id", right_on="event_id_2", suffixes=('', ''))

                other_cols = list(
                    x for x in joined_df.columns if
                    x.endswith("_2") and not x.startswith("@@")
                    and not x.startswith("event_") and not x.startswith(col))

                allowed_cols = ["event_id", "event_activity", col] + other_cols

                red_joined_df = joined_df[allowed_cols]
                red_joined_df = red_joined_df.dropna(subset=[col], how="any")
                red_joined_df = red_joined_df.dropna(axis='columns', how='all')
                if len(red_joined_df) > 0:
                    if c2+"_2" in red_joined_df.columns:
                        if col not in producer_per_class:
                            producer_per_class[col] = {}
                        producer_per_class[col][c2] = dict(red_joined_df["event_activity"].value_counts())


    return {"activities_count_per_class": activities_count_per_class,
            "producer_per_class": producer_per_class}
