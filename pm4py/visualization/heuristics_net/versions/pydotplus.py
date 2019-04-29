import math
import tempfile

import pydotplus

from pm4py.visualization.common.utils import human_readable_stat


def get_corr_hex(num):
    """
    Gets correspondence between a number
    and an hexadecimal string

    Parameters
    -------------
    num
        Number

    Returns
    -------------
    hex_string
        Hexadecimal string
    """
    if num < 10:
        return str(int(num))
    elif num < 11:
        return "A"
    elif num < 12:
        return "B"
    elif num < 13:
        return "C"
    elif num < 14:
        return "D"
    elif num < 15:
        return "E"
    elif num < 16:
        return "F"


def transform_to_hex(graycolor):
    """
    Transform color to hexadecimal representation

    Parameters
    -------------
    graycolor
        Gray color (int from 0 to 255)

    Returns
    -------------
    hex_string
        Hexadecimal color
    """
    left0 = graycolor / 16
    right0 = graycolor % 16

    left00 = get_corr_hex(left0)
    right00 = get_corr_hex(right0)

    return "#" + left00 + right00 + left00 + right00 + left00 + right00


def apply(heu_net, parameters=None):
    """
    Gets a representation of an Heuristics Net

    Parameters
    -------------
    heu_net
        Heuristics net
    parameters
        Possible parameters of the algorithm, including: format

    Returns
    ------------
    gviz
        Representation of the Heuristics Net
    """
    if parameters is None:
        parameters = {}

    image_format = parameters["format"] if "format" in parameters else "png"
    deviations = parameters["deviations"] if "deviations" in parameters else None

    if deviations is None:
        deviations = {}

    graph = pydotplus.Dot(strict=True)
    corr_nodes = {}
    corr_nodes_names = {}
    inv_corr_nodes = {}
    count_nodes = 0
    count_edges = 0
    is_frequency = False

    added_objects = {}

    for node_name in heu_net.nodes:
        node = heu_net.nodes[node_name]
        node_occ = node.node_occ
        graycolor = transform_to_hex(max(255 - math.log(node_occ) * 9, 0))
        if node.node_type == "frequency":
            is_frequency = True
            n = pydotplus.Node(name=node_name, shape="box", style="filled",
                               label=node_name + " (" + str(node_occ) + ")", fillcolor=graycolor)
        else:
            n = pydotplus.Node(name=node_name, shape="box", style="filled",
                               label=node_name, fillcolor=graycolor)
        count_nodes = count_nodes + 1
        corr_nodes[node] = n
        inv_corr_nodes[n] = node
        corr_nodes_names[node_name] = n
        graph.add_node(n)

        added_objects[node.get_label()] = n

    # gets max arc value
    max_arc_value = -1
    for node_name in heu_net.nodes:
        node = heu_net.nodes[node_name]
        for other_node in node.output_connections:
            if other_node in corr_nodes:
                for edge in node.output_connections[other_node]:
                    max_arc_value = max(max_arc_value, edge.repr_value)

    for node_name in heu_net.nodes:
        node = heu_net.nodes[node_name]
        for other_node in node.output_connections:
            if other_node in corr_nodes:
                for edge in node.output_connections[other_node]:
                    this_pen_width = 1.0 + math.log(1 + edge.repr_value) / 11.0
                    repr_value = str(edge.repr_value)
                    if edge.net_name:
                        if node.node_type == "frequency":
                            label = edge.net_name + " (" + repr_value + ")"
                        else:
                            label = edge.net_name + " (" + human_readable_stat(repr_value) + ")"
                    else:
                        if node.node_type == "frequency":
                            label = repr_value
                        else:
                            label = human_readable_stat(repr_value)

                    if corr_nodes[node] == corr_nodes[other_node] or len(deviations) == 0:
                        e = pydotplus.Edge(src=corr_nodes[node], dst=corr_nodes[other_node],
                                           label=label,
                                           color=edge.repr_color,
                                           fontcolor=edge.repr_color, penwidth=this_pen_width)
                    else:
                        n2 = pydotplus.Node(name=edge.get_label(), label="", width=0.1, height=0.1, fixedsize=True)
                        graph.add_node(n2)

                        e = pydotplus.Edge(src=corr_nodes[node], dst=n2,
                                           label="",
                                           color=edge.repr_color,
                                           fontcolor=edge.repr_color, penwidth=this_pen_width)
                        e2 = pydotplus.Edge(src=n2, dst=corr_nodes[other_node],
                                            label=label,
                                            color=edge.repr_color,
                                            fontcolor=edge.repr_color, penwidth=this_pen_width)

                        added_objects[edge.get_label()] = n2
                        graph.add_edge(e2)

                    graph.add_edge(e)

                    count_edges = count_edges + 1

    corr_nodes_stri = {n.node_name: corr_nodes[n] for n in corr_nodes}

    for index, sa_list in enumerate(heu_net.start_activities):
        effective_sa_list = [n for n in sa_list if n in corr_nodes_names]
        if effective_sa_list:
            start_i = pydotplus.Node(name="start_" + str(index), label="→", color=heu_net.default_edges_color[index],
                                     fontsize="32", fontcolor="#FFFFFF", fillcolor=heu_net.default_edges_color[index],
                                     style="filled")
            graph.add_node(start_i)
            added_objects[heu_net.net_name[index] + "@@START"] = start_i
            for node_name in effective_sa_list:
                sa = corr_nodes_names[node_name]
                if type(heu_net.start_activities[index]) is dict:
                    if is_frequency:
                        occ = heu_net.start_activities[index][node_name]
                        this_pen_width = 1.0 + math.log(1 + occ) / 11.0
                        if heu_net.net_name[index]:
                            label = heu_net.net_name[index] + " (" + str(occ) + ")"
                        else:
                            label = str(occ)
                    else:
                        this_pen_width = 1.0
                        label = heu_net.net_name[index]
                else:
                    this_pen_width = 1.0
                    label = heu_net.net_name[index]

                if len(deviations) == 0:
                    e = pydotplus.Edge(src=start_i, dst=sa, label=label,
                                       color=heu_net.default_edges_color[index],
                                       fontcolor=heu_net.default_edges_color[index], penwidth=this_pen_width)
                else:
                    this_sea_edge_label = heu_net.net_name[index] + "@@START@@" + inv_corr_nodes[sa].node_name

                    n2 = pydotplus.Node(name=this_sea_edge_label, label="", width=0.1, height=0.1, fixedsize=True)
                    graph.add_node(n2)

                    e = pydotplus.Edge(src=start_i, dst=n2, label=label,
                                       color=heu_net.default_edges_color[index],
                                       fontcolor=heu_net.default_edges_color[index], penwidth=this_pen_width)
                    e2 = pydotplus.Edge(src=n2, dst=sa, label="",
                                        color=heu_net.default_edges_color[index],
                                        fontcolor=heu_net.default_edges_color[index], penwidth=this_pen_width)

                    added_objects[this_sea_edge_label] = n2
                    graph.add_edge(e2)
                graph.add_edge(e)
                count_edges = count_edges + 1

    for index, ea_list in enumerate(heu_net.end_activities):
        effective_ea_list = [n for n in ea_list if n in corr_nodes_names]
        if effective_ea_list:
            end_i = pydotplus.Node(name="end_" + str(index), label="□", color=heu_net.default_edges_color[index],
                                   fillcolor=heu_net.default_edges_color[index], fontcolor="#FFFFFF", fontsize="32",
                                   style="filled")
            added_objects[heu_net.net_name[index] + "@@END"] = end_i
            graph.add_node(end_i)
            for node_name in effective_ea_list:
                ea = corr_nodes_names[node_name]
                if type(heu_net.end_activities[index]) is dict:
                    if is_frequency:
                        occ = heu_net.end_activities[index][node_name]
                        this_pen_width = 1.0 + math.log(1 + occ) / 11.0
                        if heu_net.net_name[index]:
                            label = heu_net.net_name[index] + " (" + str(occ) + ")"
                        else:
                            label = str(occ)
                    else:
                        label = heu_net.net_name[index]
                        this_pen_width = 1.0
                else:
                    label = heu_net.net_name[index]
                    this_pen_width = 1.0

                if len(deviations) == 0:
                    e = pydotplus.Edge(src=ea, dst=end_i, label=label,
                                       color=heu_net.default_edges_color[index],
                                       fontcolor=heu_net.default_edges_color[index], penwidth=this_pen_width)
                else:
                    this_sea_edge_label = heu_net.net_name[index] + "@@" + inv_corr_nodes[ea].node_name + "@@END"

                    n2 = pydotplus.Node(name=this_sea_edge_label,
                                        label="", width=0.1, height=0.1, fixedsize=True)
                    graph.add_node(n2)

                    e = pydotplus.Edge(src=ea, dst=n2, label="",
                                       color=heu_net.default_edges_color[index],
                                       fontcolor=heu_net.default_edges_color[index], penwidth=this_pen_width)
                    e2 = pydotplus.Edge(src=n2, dst=end_i, label=label,
                                        color=heu_net.default_edges_color[index],
                                        fontcolor=heu_net.default_edges_color[index], penwidth=this_pen_width)

                    added_objects[this_sea_edge_label] = n2
                    graph.add_edge(e2)
                graph.add_edge(e)
                count_edges = count_edges + 1

    # add places
    activities_preset_of = {}
    classes_preset_of = {}

    for index, data in enumerate(heu_net.data):
        class_name = heu_net.net_name[index]
        data = heu_net.data[index]

        for index2, place in enumerate(data):
            input_activities = place[0]
            output_activities = place[1]
            place_name = class_name + "@@" + place[2].name

            place = pydotplus.Node(name=place_name, label="", style="filled",
                                   fillcolor=heu_net.default_edges_color[index],
                                   color=heu_net.default_edges_color[index])
            graph.add_node(place)
            added_objects[place_name] = place

            for act in input_activities:
                e = pydotplus.Edge(style="dashed", color=heu_net.default_edges_color[index], src=corr_nodes_stri[act],
                                   dst=place, label=heu_net.net_name[index],
                                   fontcolor=heu_net.default_edges_color[index])
                graph.add_edge(e)

            for act in output_activities:
                e = pydotplus.Edge(style="dashed", color=heu_net.default_edges_color[index], src=place,
                                   dst=corr_nodes_stri[act], label=heu_net.net_name[index],
                                   fontcolor=heu_net.default_edges_color[index])
                graph.add_edge(e)
                if act not in activities_preset_of:
                    activities_preset_of[act] = set()
                if act not in classes_preset_of:
                    classes_preset_of[act] = set()
                classes_preset_of[act].add(class_name)
                for input_act in input_activities:
                    activities_preset_of[act].add(input_act)

    for act in activities_preset_of:
        if len(activities_preset_of[act]) > 1 and len(classes_preset_of[act]) > 1:
            print("MP", act, "activities_preset_of", activities_preset_of[act], "classes_preset_of",
                  classes_preset_of[act])

    if is_frequency:
        for deviation in deviations:
            content = deviation.split("%%")[0]
            involved_objects = content.split("##")
            if len(involved_objects) >= 1:
                this_perspective = involved_objects[0].split("@@")[0]
                index = heu_net.net_name.index(this_perspective)
                this_label = this_perspective + " (dev=" + str(deviations[deviation]) + ")"

                obj1 = None
                obj2 = None

                if len(involved_objects) == 1:
                    if involved_objects[0] in added_objects:
                        obj1 = added_objects[involved_objects[0]]
                        obj2 = added_objects[involved_objects[0]]
                else:
                    if involved_objects[0] in added_objects and involved_objects[1] in added_objects:
                        obj1 = added_objects[involved_objects[0]]
                        obj2 = added_objects[involved_objects[1]]

                if obj1 is not None and obj2 is not None:
                    e3 = pydotplus.Edge(style="dashed", color=heu_net.default_edges_color[index],
                                        fontcolor=heu_net.default_edges_color[index], src=obj1, dst=obj2,
                                        label=this_label, fontsize=7)
                    graph.add_edge(e3)

    print(count_nodes, count_edges)

    file_name = tempfile.NamedTemporaryFile(suffix='.' + image_format)
    file_name.close()
    graph.write(file_name.name, format=image_format)
    return file_name
