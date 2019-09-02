from graphviz import Digraph
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave
import uuid
import tempfile

COLORS = ["#05B202", "#A13CCD", "#39F6C0", "#BA0D39", "#E90638", "#07B423", "#306A8A", "#678225", "#2742FE", "#4C9A75",
          "#4C36E9", "#7DB022", "#EDAC54", "#EAC439", "#EAC439", "#1A9C45", "#8A51C4", "#496A63", "#FB9543", "#2B49DD",
          "#13ADA5", "#2DD8C1", "#2E53D7", "#EF9B77", "#06924F", "#AC2C4D", "#82193F", "#0140D3"]

def apply(model, parameters=None):
    if parameters is None:
        parameters = {}

    image_format = "png"
    if "format" in parameters:
        image_format = parameters["format"]

    filename = tempfile.NamedTemporaryFile(suffix='.gv').name
    g = Digraph("", filename=filename, engine='dot', graph_attr={'bgcolor': 'transparent'})

    cluster_corr = {}
    cluster_acti_corr = {}

    perspectives = sorted(list(model.node_freq.keys()))
    for index, p in enumerate(perspectives):
        color = COLORS[index % len(COLORS)]

        with g.subgraph(name='cluster_' + p) as c:
            cluster_corr[p] = c
            cluster_acti_corr[p] = {}

            c.attr(style='filled')
            c.attr(color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            c.attr(label='class: ' + p)

            for act in model.node_freq[p]:
                this_uuid = str(uuid.uuid4())
                c.node(this_uuid, act + "(" + str(model.node_freq[p][act]) + ")", fillcolor=color, style="filled")
                cluster_acti_corr[p][act] = this_uuid

    for index, persp in enumerate(perspectives):
        color = COLORS[index % len(COLORS)]

        for edge in model.edge_freq[persp]:

            act1 = cluster_acti_corr[persp][edge.split("@@")[0]]
            act2 = cluster_acti_corr[persp][edge.split("@@")[1]]

            g.edge(act1, act2, persp + " ("+str(model.edge_freq[persp][edge])+")", color=color, fontcolor=color)


    g.attr(overlap='false')
    g.attr(fontsize='11')

    g.format = image_format

    return g