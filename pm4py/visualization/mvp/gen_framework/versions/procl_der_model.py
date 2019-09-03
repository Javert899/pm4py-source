from graphviz import Digraph
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave
import uuid
import tempfile

def apply(model, parameters=None):
    if parameters is None:
        parameters = {}

    image_format = "png"
    if "format" in parameters:
        image_format = parameters["format"]

    filename = tempfile.NamedTemporaryFile(suffix='.gv').name
    g = Digraph("", filename=filename, engine='dot', graph_attr={'bgcolor': 'transparent'})

    activities = {}
    cluster_corr = {}
    all_objs = {}

    for p in model.model_inductive:
        net, im, fm = model.model_inductive[p]
        activities[p] = {}

        with g.subgraph(name='cluster_' + p) as c:
            cluster_corr[p] = c
            c.attr(style='filled')
            c.attr(color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            c.attr(label='class: ' + p)

            for pl in net.places:
                this_uuid = str(uuid.uuid4())
                if pl in im:
                    c.node(this_uuid, "", shape="circle", fillcolor="#32CD32")
                elif pl in fm:
                    c.node(this_uuid, "", shape="circle", fillcolor="#FFA500")
                else:
                    c.node(this_uuid, "", shape="circle")
                all_objs[pl] = this_uuid

            for tr in net.transitions:
                this_uuid = str(uuid.uuid4())
                if tr.label is None:
                    c.node(this_uuid, "", shape="box", fillcolor="#000000", style="filled")
                else:
                    c.node(this_uuid, tr.label, shape="box")
                    activities[p][tr.label] = this_uuid
                all_objs[tr] = this_uuid

            for arc in net.arcs:
                c.edge(all_objs[arc.source], all_objs[arc.target])

    g.attr(overlap='false')
    g.attr(fontsize='11')

    g.format = image_format

    return g