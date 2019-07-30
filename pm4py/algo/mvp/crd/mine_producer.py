from pm4py.algo.mvp.crd import get_first_for_object


def mine_producer(df, parameters=None):
    cols = [x for x in df.columns if not x.startswith("event_")]
    df["@@index"] = df.index
    first_obj_df = get_first_for_object.get_first(df, parameters=parameters)

    joined_df = df.merge(first_obj_df, left_on="event_id", right_on="event_id", suffixes=('', '_2'))

    new_cols = joined_df.columns

    activities_count_per_class = {}
    producer_per_class = {}

    for col in cols:
        allowed_cols = ["event_id", "event_activity", col] + list(x for x in new_cols if
                                                                  x.endswith("_2") and not x.startswith(
                                                                      col) and not x.startswith(
                                                                      "event_") and not x.startswith("@@"))
        red_joined_df = joined_df[allowed_cols]
        activities_count_per_class[col] = dict(red_joined_df.groupby("event_id").first()["event_activity"].value_counts())
        red_joined_df = red_joined_df.dropna(subset=[col], how="any").dropna(axis='columns', how='all')

        new_cols_with_2 = [x for x in red_joined_df.columns if x.endswith("_2")]

        for c2 in new_cols_with_2:
            red_joined_df_red = red_joined_df[["event_id", "event_activity", col, c2]].dropna()

            if len(red_joined_df_red) > 0:
                if col not in producer_per_class:
                    producer_per_class[col] = {}
                producer_per_class[col][c2] = dict(red_joined_df_red["event_activity"].value_counts())

    return {"activities_count_per_class": activities_count_per_class,
            "producer_per_class": producer_per_class}

