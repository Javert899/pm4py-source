from copy import copy
from datetime import datetime
from dateutil import parser

import pandas as pd


def apply(file_path, parameters=None):
    """
    Apply the importing of a XOC file

    Parameters
    ------------
    file_path
        Path to the XOC file
    parameters
        Import parameters

    Returns
    ------------
    dataframe
        Dataframe
    """
    if parameters is None:
        parameters = {}

    import_timestamp = parameters["import_timestamp"] if "import_timestamp" in parameters else True

    F = open(file_path, "r")
    content = F.read()
    F.close()
    events = content.split("<event>")
    stream = []
    stream_strings = []
    i = 1
    while i < len(events) - 1:
        event_id = events[i].split("\"id\" value=\"")[1].split("\"")[0]
        event_activity = events[i].split("\"activity\" value=\"")[1].split("\"")[0]
        event_timestamp0 = events[i].split("\"timestamp\" value=\"")[1].split("\"")[0].replace(" CET", "")
        event_timestamp = None
        if import_timestamp:
            try:
                event_timestamp = parser.parse(event_timestamp0)
            except:
                pass
        if event_timestamp is not None:
            event_dictio = {"event_id": event_id, "event_activity": event_activity, "event_timestamp": event_timestamp}
        else:
            event_dictio = {"event_id": event_id, "event_activity": event_activity}
        references = events[i].split("<references>")[1].split("</references>")[0].split("<object>")
        j = 1
        while j < len(references):
            this_event_dictio = copy(event_dictio)
            object_id = references[j].split("\"id\" value=\"")[1].split("\"")[0]
            object_class = references[j].split("\"class\" value=\"")[1].split("\"")[0]
            this_event_dictio[object_class] = object_id
            this_event_dictio_stri = str(this_event_dictio)
            if this_event_dictio_stri not in stream_strings:
                stream.append(this_event_dictio)
                stream_strings.append(this_event_dictio_stri)
            j = j + 1
        i = i + 1
    dataframe = pd.DataFrame.from_dict(stream)
    return dataframe
