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

    filename = "temp.gv"
    g = Digraph("", filename=filename, engine='dot', graph_attr={'bgcolor': 'transparent'})

    nodes = {}
    subgraphs = {}
    all_objs = {}

    for p in input_object:
        if not p.startswith("@@"):
            nodes[p] = {}
            with g.subgraph(name='cluster_' + p) as c:
                c.attr(label='class: ' + p)
                subgraphs[p] = c
                c.attr(style='filled')
                c.attr(color='lightgrey')
                c.node_attr.update(style='filled', color='white')
                for pl in input_object[p]["net_inductive"][0].places:
                    this_uuid = str(uuid.uuid4())
                    c.node(this_uuid, "", shape="circle")
                    all_objs[pl] = this_uuid
                for tr in input_object[p]["net_inductive"][0].transitions:
                    this_uuid = str(uuid.uuid4())
                    if tr.label is None:
                        c.node(this_uuid, "", shape="box", fillcolor="#000000", style="filled")
                    else:
                        c.node(this_uuid, tr.label, shape="box")
                        nodes[tr.label] = this_uuid
                    all_objs[tr] = this_uuid
                for arc in input_object[p]["net_inductive"][0].arcs:
                    c.edge(all_objs[arc.source], all_objs[arc.target])

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
