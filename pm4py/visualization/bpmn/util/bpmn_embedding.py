from pm4py.objects.bpmn.importer import bpmn_python_consts


def embed_info_into_bpmn(bpmn_graph, bpmn_aggreg_statistics, decoration):
    """
    Embed information inside the BPMN graph

    Parameters
    -----------
    bpmn_graph
        BPMN graph object
    bpmn_aggreg_statistics
        Element-wise statistics that should be represented on the BPMN graph
    decoration
        Type of decoration included

    Returns
    -----------
    bpmn_graph
        BPMN graph object
    """
    for string_el in bpmn_aggreg_statistics:
        statistics = bpmn_aggreg_statistics[string_el]
        el = eval(string_el)
        el_id = el['id']
        el_type = "task" if ("type" in el and el["type"] == "task") else "arc"

        if el_type == "arc":
            flow = bpmn_graph.get_flow_by_id(el_id)
            if bpmn_python_consts.Consts.decorations not in flow[2]:
                flow[2][bpmn_python_consts.Consts.decorations] = []
            for stat in statistics:
                stat_value = statistics[stat]
                flow[2][bpmn_python_consts.Consts.decorations].append([decoration + "_" + stat, str(stat_value)])
        elif el_type == "task":
            node = bpmn_graph.get_node_by_id(el_id)
            if bpmn_python_consts.Consts.decorations not in node[1]:
                node[1][bpmn_python_consts.Consts.decorations] = []
            for stat in statistics:
                stat_value = statistics[stat]
                node[1][bpmn_python_consts.Consts.decorations].append([decoration + "_" + stat, str(stat_value)])

    return bpmn_graph
