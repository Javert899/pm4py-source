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


    filename = tempfile.NamedTemporaryFile(suffix='.gv')
    g = Digraph("", filename=filename.name, engine='dot', graph_attr={'bgcolor': 'transparent'})

    nodes = {}

    for p in input_object:
        nodes[p] = {}
        with g.subgraph(name='cluster_'+p) as c:
            c.attr(style='filled')
            c.attr(color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            for a in input_object[p]["activities_count"]:
                this_uuid = str(uuid.uuid4())
                c.node(this_uuid, a + " (" + str(input_object[p]["activities_count"][a]) + ")")
                nodes[p][a] = this_uuid
            for x,y in input_object[p]["dfg"].items():
                s = x[0]
                t = x[1]
                c.edge(nodes[p][s], nodes[p][t], label=str(y))
            c.attr(label='class: '+p)

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
