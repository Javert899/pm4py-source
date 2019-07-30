import pandas as pd

def get_first(df, parameters=None):
    columns = [x for x in df.columns if not x.startswith("event_")]

    all_dfs = []

    for c in columns:
        red_df = df.groupby(c).first()

        all_dfs.append(red_df)

    return pd.concat(all_dfs).sort_values(['event_timestamp', 'event_id'])
