def apply(df, parameters=None):
    return dict(df.groupby("event_id").first()["event_activity"].value_counts())
