import pandas as pd

def get_last(df, parameters=None):
    if parameters is None:
        parameters = {}

    target_col = parameters["target_col"] if "target_col" in parameters else None

    columns = [x for x in df.columns if not x.startswith("event_")]

    all_dfs = []

    for c in columns:
        if target_col is None or target_col == c:
            red_df = df.groupby(c).last()

            all_dfs.append(red_df)

    return pd.concat(all_dfs).sort_values(['event_timestamp', 'event_id']).reset_index()
