import networkx as nx
import matplotlib.pyplot as plt


def apply(dfg, parameters=None):
    """
    Apply DFG link prediction

    Parameters
    -------------
    dfg
        DFG
    parameters
        Parameters of the algorithm:
         algorithm, threshold

    Returns
    -------------
    dfg
        Enriched DFG
    """
    if parameters is None:
        parameters = {}

    algorithm = parameters["algorithm"] if "algorithm" in parameters else "resource_allocation_index"
    # for test purposes: if it is provided, then the optimal threshold to add missing edges is determined
    optimal_dfg = parameters["optimal_dfg"] if "optimal_dfg" in parameters else []

    graph = transform_to_nx_graph(dfg)
    if algorithm == "resource_allocation_index":
        print("0 ", algorithm)
        preds = list(nx.resource_allocation_index(graph))
    elif algorithm == "jaccard_coefficient":
        print("1 ", algorithm)
        preds = list(nx.jaccard_coefficient(graph))
    elif algorithm == "adamic_adar_index":
        print("2 ", algorithm)
        preds = list(nx.adamic_adar_index(graph))
    elif algorithm == "preferential_attachment":
        print("3 ",algorithm)
        preds = list(nx.preferential_attachment(graph))

    i = 0
    while i < len(preds):
        if preds[i][0].endswith("@#@OUT") and preds[i][1].endswith("@#@IN") and preds[i][2] > 0:
            i = i + 1
            continue
        del preds[i]

    preds = sorted(preds, key=lambda x: x[2], reverse=True)

    if optimal_dfg:
        for i in range(len(preds)):
            act0 = preds[i][0].split("@#@")[0]
            act1 = preds[i][1].split("@#@")[0]

            couple = (act0, act1)

            if couple in optimal_dfg:
                print(i, "ok")
                dfg[couple] = 1
            else:
                if i > 0:
                    print("iterations: ", i, " threshold", preds[i - 1][2])
                print(couple,"not ok")
                input()
                #break

    # print(preds)

    return None


def transform_to_nx_graph(dfg):
    """
    Transform a DFG to an NX Graph

    Parameters
    -------------
    dfg
        Directly-Follows Graph

    Returns
    -------------
    graph
        NX Graph
    """
    in_activities = {}
    out_activities = {}

    G = nx.Graph()

    max_value = max(dfg.values())

    for el in dfg:
        act0 = el[0]
        act1 = el[1]

        if not act0 in in_activities:
            in_activities[act0] = act0 + "@#@IN"
            out_activities[act0] = act0 + "@#@OUT"

            G.add_node(in_activities[act0])
            G.add_node(out_activities[act0])
            G.add_edge(in_activities[act0], out_activities[act0], weight=100)

        if not act1 in in_activities:
            in_activities[act1] = act1 + "@#@IN"
            out_activities[act1] = act1 + "@#@OUT"

            G.add_node(in_activities[act1])
            G.add_node(out_activities[act1])
            G.add_edge(in_activities[act1], out_activities[act1], weight=100)

        G.add_edge(out_activities[act0], in_activities[act1], weight=10)
        #G.add_edge(in_activities[act0], out_activities[act1], weight=dfg[el])
        G.add_edge(in_activities[act0], in_activities[act1], weight=1)
        G.add_edge(out_activities[act0], out_activities[act1], weight=1)

    print("AAA")
    plt.clf()
    nx.draw(G)
    plt.savefig("ciao.png", bbox_inches="tight")
    plt.clf()

    return G
