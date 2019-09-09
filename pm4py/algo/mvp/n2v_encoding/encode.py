from pm4py.algo.mvp.utils import df_to_grouped_stream_old
import networkx
from node2vec import Node2Vec


def from_df(df, parameters=None):
    """
    Encode a database log dataframe to a node2vec representation

    Parameters
    ------------
    df
        Dataframe
    parameters
        Parameters of the algorithm

    Returns
    ------------
    rep
        Node2vec representation
    """
    if parameters is None:
        parameters = {}

    include_activities = parameters["include_activities"] if "include_activities" in parameters else True
    include_classes = parameters["include_classes"] if "include_classes" in parameters else True
    max_no_events = parameters["max_no_events"] if "max_no_events" in parameters else 10000000

    ret = {}

    ret["activities"] = set()
    ret["classes"] = set()
    ret["events"] = set()
    ret["objects"] = set()

    added_elements = set()

    G = networkx.Graph()

    grouped_stream = df_to_grouped_stream_old.apply(df, remove_common=True, include_activity_timest_in_key=True)
    keys = list(grouped_stream.keys())

    for i in range(min(len(keys), max_no_events)):
        event = keys[i]
        event_id = event[0]
        event_activity = event[1]
        event_id_name = "event="+str(event_id)+" activity="+str(event_activity)
        event_activity_name = "ACTIVITY="+str(event_activity)
        if not event_id_name in added_elements:
            added_elements.add(event_id_name)
            G.add_node(event_id_name)
        ret["events"].add(event_id_name)
        if include_activities:
            if not event_activity_name in added_elements:
                added_elements.add(event_activity_name)
                G.add_node(event_activity_name)
            ret["activities"].add(event_activity_name)
            G.add_edge(event_id_name, event_activity_name)
        for object in grouped_stream[event]:
            items = [(k, v) for k, v in object.items()]
            for item in items:
                object_id = item[1]
                object_class = item[0]
                object_id_name = "object="+str(object_id)+" class="+str(object_class)
                object_class_name = "CLASS="+str(object_class)
                if not object_id_name in added_elements:
                    added_elements.add(object_id_name)
                    G.add_node(object_id_name)
                ret["objects"].add(object_id_name)
                if include_classes:
                    if not object_class_name in added_elements:
                        added_elements.add(object_class_name)
                        G.add_node(object_class_name)
                    ret["classes"].add(object_class_name)
                    G.add_edge(object_id_name, object_class_name)
                G.add_edge(event_id_name, object_id_name)

    # Generate walks
    print("generating n2v")
    node2vec = Node2Vec(G, dimensions=20, walk_length=16, num_walks=100)

    print("starting fitting")
    # Learn embeddings
    model = node2vec.fit(window=10, min_count=1)

    ret["model"] = model
    ret["graph"] = G

    return ret
