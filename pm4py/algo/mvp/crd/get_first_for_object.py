import pandas as pd

def get_first(df, parameters=None):
    if parameters is None:
        parameters = {}

    target_col = parameters["target_col"] if "target_col" in parameters else None
    positive = parameters["positive"] if "positive" in parameters else True

    columns = [x for x in df.columns if not x.startswith("event_")]

    if not positive:
        df["@@index"] = df.index

    all_dfs = []

    for c in columns:
        if target_col is None or target_col == c:
            red_df = df.groupby(c).first()

            all_dfs.append(red_df)

    if positive:
        return pd.concat(all_dfs).sort_values(['event_timestamp', 'event_id']).reset_index()
    else:
        i1 = df.index
        i2 = pd.concat(all_dfs).set_index("@@index").index

        return df[~i1.isin(i2)].reset_index()
