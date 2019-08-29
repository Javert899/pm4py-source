import pandas as pd

def apply(df, model, rel_ev, rel_act, parameters=None):
    if parameters is None:
        parameters = {}

    df_list = []

    class_dest = {}

    for act in model.map:
        target = model.map[act]
        if target not in class_dest:
            class_dest[target] = []
        class_dest[target].append(act)

    for cl in class_dest:
        red_df = df[["event_id", "event_activity", "event_timestamp", cl]].dropna()
        red_df = red_df[red_df["event_activity"].isin(class_dest[cl])]

        df_list.append(red_df)

    new_df = pd.concat(df_list)

    return dict(new_df.groupby("event_id").first()["event_activity"].value_counts())
