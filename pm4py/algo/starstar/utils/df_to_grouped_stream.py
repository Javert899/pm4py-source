def apply(df):
    """
    Dataframe to grouped stream

    Parameters
    -------------
    df
        Dataframe

    Returns
    -------------
    grouped_stream
        Grouped stream of events
    """
    stream = df.to_dict('r')
    grouped_stream = {}

    i = 0
    while i < len(stream):
        keys = list(stream[i].keys())
        for key in keys:
            if str(stream[i][key]) == "nan":
                del stream[i][key]
        event_id = stream[i]["event_id"]
        if event_id not in grouped_stream:
            grouped_stream[event_id] = []
        grouped_stream[event_id].append(stream[i])
        i = i + 1

    return grouped_stream
