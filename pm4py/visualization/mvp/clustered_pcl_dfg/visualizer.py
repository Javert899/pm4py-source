from graphviz import Digraph
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave
import uuid
import tempfile


def apply(input_object, parameters=None):
    if parameters is None:
        parameters = {}

    image_format = "png"
    if "format" in parameters:
        image_format = parameters["format"]

    # filename = tempfile.NamedTemporaryFile(suffix='.gv')
    filename = "temp.gv"
    g = Digraph("", filename=filename, engine='dot', graph_attr={'bgcolor': 'transparent'})

    nodes = {}
    subgraphs = {}

    for p in input_object:
        if not p.startswith("@@"):
            nodes[p] = {}
            with g.subgraph(name='cluster_' + p) as c:
                c.attr(style='filled')
                c.attr(color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                for a in input_object[p]["activities_count"]:
                    this_uuid = str(uuid.uuid4())
                    c.node(this_uuid, a + " (" + str(input_object[p]["activities_count"][a]) + ")")
                    nodes[p][a] = this_uuid
                for x, y in input_object[p]["dfg"].items():
                    s = x[0]
                    t = x[1]
                    c.edge(nodes[p][s], nodes[p][t], label=str(y))
                c.attr(label='class: ' + p)
                subgraphs[p] = c
                start_uuid = str(uuid.uuid4())
                end_uuid = str(uuid.uuid4())
                nodes[p]["@@startnode"] = start_uuid
                nodes[p]["@@endnode"] = end_uuid
                c.node(start_uuid, "", style='filled', shape='circle', fillcolor="#32CD32",
                       fontcolor="#32CD32")
                c.node(end_uuid, "", style='filled', shape='circle', fillcolor="#FFA500", fontcolor="#FFA500")
                for a in input_object[p]["start_activities"]:
                    if a in nodes[p]:
                        c.edge(start_uuid, nodes[p][a], label=str(input_object[p]["start_activities"][a]))
                for a in input_object[p]["end_activities"]:
                    if a in nodes[p]:
                        c.edge(nodes[p][a], end_uuid, label=str(input_object[p]["end_activities"][a]))

    for p1 in input_object["@@producers"]["producer_per_class"]:
        for p2 in input_object["@@producers"]["producer_per_class"][p1]:
            for act in input_object["@@producers"]["producer_per_class"][p1][p2]:
                count = input_object["@@producers"]["producer_per_class"][p1][p2][act]
                if p1 in nodes and p2 in nodes and act in nodes[p1] and act in nodes[p2]:
                    g.edge(nodes[p1][act], nodes[p2][act], style="dashed", xlabel="count=" + str(count),
                           color="#32CD32", fontcolor="#32CD32")
                    pass

    g.attr(overlap='false')
    g.attr(fontsize='11')

    g.format = image_format

    return g


def save(gviz, output_file_path):
    """
    Save the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    output_file_path
        Path where the GraphViz output should be saved
    """
    gsave.save(gviz, output_file_path)


def view(gviz):
    """
    View the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    """
    return gview.view(gviz)
