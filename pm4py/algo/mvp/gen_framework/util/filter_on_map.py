import pandas as pd

DEFAULT_ACTIVITY_KEY = "event_activity"

def apply(df, map, activity_key=DEFAULT_ACTIVITY_KEY, parameters=None):
    if parameters is None:
        parameters = {}

    df_list = []

    class_dest = {}

    for act in map:
        target = map[act]
        if target not in class_dest:
            class_dest[target] = []
        class_dest[target].append(act)

    for cl in class_dest:
        if activity_key == DEFAULT_ACTIVITY_KEY:
            cols_to_include = ["event_id", "event_activity", "event_timestamp", cl]
        else:
            cols_to_include0 = ["event_id", "event_activity", "event_timestamp", cl]
            cols_to_include = [x for x in cols_to_include0] + [x+"_2" for x in cols_to_include0]
        red_df = df[cols_to_include].dropna()
        red_df = red_df[red_df[activity_key].isin(class_dest[cl])]

        df_list.append(red_df)

    new_df = pd.concat(df_list)

    return new_df
