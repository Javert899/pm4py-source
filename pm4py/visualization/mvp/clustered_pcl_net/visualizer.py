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
                    if pl in input_object[p]["net_inductive"][1]:
                        c.node(this_uuid, "", shape="circle", fillcolor="#32CD32")
                    elif pl in input_object[p]["net_inductive"][2]:
                        c.node(this_uuid, "", shape="circle", fillcolor="#FFA500")
                    else:
                        c.node(this_uuid, "", shape="circle")
                    all_objs[pl] = this_uuid
                for tr in input_object[p]["net_inductive"][0].transitions:
                    this_uuid = str(uuid.uuid4())
                    if tr.label is None:
                        c.node(this_uuid, "", shape="box", fillcolor="#000000", style="filled")
                    else:
                        c.node(this_uuid, tr.label, shape="box")
                        nodes[p][tr.label] = this_uuid
                    all_objs[tr] = this_uuid
                for arc in input_object[p]["net_inductive"][0].arcs:
                    c.edge(all_objs[arc.source], all_objs[arc.target])

    all_prod_rel = set()
    all_prod_rel_det = set()

    for p1 in input_object["@@producers"]["producer_per_class"]:
        for p2 in input_object["@@producers"]["producer_per_class"][p1]:
            for act in input_object["@@producers"]["producer_per_class"][p1][p2]:
                if p1 in nodes and p2 in nodes and act in nodes[p1] and act in nodes[p2] and act in \
                        input_object["@@producers"]["relations_per_class"][p1][p2]:
                    left = input_object["@@producers"]["relations_per_class"][p1][p2][act][0]
                    right = input_object["@@producers"]["relations_per_class"][p1][p2][act][1]
                    classes_ordered = sorted([[p1, left], [p2, right]], key=lambda x: x[0])
                    if not ((act, classes_ordered[0][0], classes_ordered[1][0]) in all_prod_rel):
                        all_prod_rel.add((act, classes_ordered[0][0], classes_ordered[1][0]))
                        all_prod_rel_det.add((act, p1, p2, left, right))

    all_rel = set()
    all_rel_det = set()

    for p1 in input_object["@@ports"]:
        for p2 in input_object["@@ports"][p1]:
            for act2 in input_object["@@ports"][p1][p2]:
                for act in input_object["@@ports"][p1][p2][act2]:
                    if act in nodes[p1] and act2 in nodes[p1] and act in nodes[p2] and act2 in nodes[p2]:
                        rel = input_object["@@ports"][p1][p2][act2][act]
                        classes_ordered = sorted([p1, p2])

                        if not (act, act2, classes_ordered[0], classes_ordered[1]) in all_rel:
                            if p1 in input_object["@@producers"]["producer_per_class"] and p2 in \
                                    input_object["@@producers"]["producer_per_class"][p1] and act in \
                                    input_object["@@producers"]["producer_per_class"][p1][p2]:
                                all_rel_det.add((act, act2, p1, p2, rel))
                                all_rel.add((act, act2, classes_ordered[0], classes_ordered[1]))

    mapp = {}

    for prod_rel in all_prod_rel_det:
        act = prod_rel[0]
        p1 = prod_rel[1]
        p2 = prod_rel[2]
        left = prod_rel[3]
        right = prod_rel[4]

        if act in nodes[p1] and act in nodes[p2]:
            print("2", act, p1, p2, left, right)

            mapp[(act, p1, p2)] = (left, right)

            this_uuid1 = str(uuid.uuid4())
            node1 = g.node(this_uuid1, left, shape='box', style="filled", fillcolor="#32CD32")
            this_uuid2 = str(uuid.uuid4())
            node2 = g.node(this_uuid2, right, shape='box', style="filled", fillcolor="#32CD32")

            g.edge(nodes[p1][act], this_uuid1, dir="none", color="#32CD32")
            g.edge(this_uuid2, nodes[p2][act], dir="none", color="#32CD32")
            g.edge(this_uuid1, this_uuid2, xlabel="init (" + p1 + "," + p2 + ")", dir="none", color="#32CD32")

    for rel in all_rel_det:
        act1 = rel[0]
        act2 = rel[1]
        p1 = rel[2]
        p2 = rel[3]
        r = rel[4]

        # print(act1, act2, p1, p2, r)

        if act2 in nodes[p1] and act2 in nodes[p2]:
            if (act1, p1, p2) in mapp:
                target_color = "#666666"

                if p1 in input_object["@@consumers"]["consumer_per_class"] and p2 in input_object["@@consumers"]["consumer_per_class"][p1] and act2 in input_object["@@consumers"]["consumer_per_class"][p1][p2]:
                    target_color = "#FFA500"

                this_uuid1 = str(uuid.uuid4())
                node1 = g.node(this_uuid1, mapp[(act1, p1, p2)][0], shape='box', style="filled", fillcolor=target_color)
                this_uuid2 = str(uuid.uuid4())
                node2 = g.node(this_uuid2, mapp[(act1, p1, p2)][1], shape='box', style="filled", fillcolor=target_color)

                g.edge(nodes[p1][act2], this_uuid1, dir="none", color=target_color)
                g.edge(this_uuid2, nodes[p2][act2], dir="none", color=target_color)

                g.edge(this_uuid1, this_uuid2, xlabel=r + " (" + p1 + "," + p2 + ")", dir="none", color=target_color)

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
