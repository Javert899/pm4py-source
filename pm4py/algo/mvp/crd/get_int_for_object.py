import pandas as pd

def get_int(df, parameters=None):
    if parameters is None:
        parameters = {}

    columns = [x for x in df.columns if not x.startswith("event_")]

    target_col = parameters["target_col"] if "target_col" in parameters else None

    df["@@index"] = df.index

    all_first_dfs = []
    all_last_dfs = []

    for c in columns:
        if target_col is None or target_col == c:
            all_first_dfs.append(df.groupby(c).first())
            all_last_dfs.append(df.groupby(c).last())

    concat_first = pd.concat(all_first_dfs).sort_values(['event_timestamp', 'event_id'])
    concat_last = pd.concat(all_last_dfs).sort_values(['event_timestamp', 'event_id'])

    i1 = df.index
    i2 = concat_first.set_index("@@index").index
    i3 = concat_last.set_index("@@index").index

    return df[~i1.isin(i2) & ~i1.isin(i3)].sort_values(['event_timestamp', 'event_id']).reset_index()
