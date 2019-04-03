from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri.utils import add_arc_from_to


def apply(mvp, parameters=None):
    """
    Apply DFG mining

    Parameters
    ------------
    mvp
        Multiple Viewpoint Model
    parameters
        Parameters of the algorithm

    Returns
    ------------
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    """
    if parameters is None:
        parameters = {}

    perspectives = parameters["perspectives"]

    net = PetriNet("")
    im = Marking()
    fm = Marking()

    corr_places = {}

    master_source = PetriNet.Place("master_source")
    net.places.add(master_source)
    im[master_source] = 1
    master_so_ht = PetriNet.Transition("master_so_ht")
    net.transitions.add(master_so_ht)
    add_arc_from_to(master_source, master_so_ht, net)
    master_sink = PetriNet.Place("master_sink")
    fm[master_sink] = 1
    net.places.add(master_sink)
    master_si_ht = PetriNet.Transition("master_si_ht")
    net.transitions.add(master_si_ht)
    add_arc_from_to(master_si_ht, master_sink, net)
    added_arcs = set()

    for index, perspective in enumerate(perspectives):
        start_activities = list(mvp[perspective].start_activities[0].keys())
        end_activites = list(mvp[perspective].end_activities[0].keys())
        nodes = mvp[perspective].nodes

        source = PetriNet.Place("so_" + perspective)
        net.places.add(source)
        ht_source = PetriNet.Transition("htso_"+perspective)
        net.transitions.add(ht_source)
        add_arc_from_to(master_so_ht, source, net)
        add_arc_from_to(source, ht_source, net)

        for act in start_activities:
            if act not in corr_places:
                corr_places[act] = PetriNet.Place("p_"+act)
                net.places.add(corr_places[act])
            add_arc_from_to(ht_source, corr_places[act], net)

        sink = PetriNet.Place("si_" + perspective)
        net.places.add(sink)
        ht_sink = PetriNet.Transition("htsi_"+perspective)
        net.transitions.add(ht_sink)
        add_arc_from_to(ht_sink, sink, net)
        add_arc_from_to(sink, master_si_ht, net)

        for act in end_activites:
            if act not in corr_places:
                corr_places[act] = PetriNet.Place("p_"+act)
                net.places.add(corr_places[act])
            add_arc_from_to(corr_places[act], ht_sink, net)

        for i1, n1 in enumerate(nodes):
            if n1 not in corr_places:
                corr_places[n1] = PetriNet.Place("p1_"+n1)
                net.places.add(corr_places[n1])
            for i2, n2n in enumerate(nodes[n1].output_connections):
                n2 = n2n.node_name
                if n2 not in corr_places:
                    corr_places[n2] = PetriNet.Place("p2_"+n2)
                    net.places.add(corr_places[n2])
                trans = PetriNet.Transition("tr_"+str(n1)+"_"+str(n2), n1)
                net.transitions.add(trans)
                if (str(n1), "tr_"+str(n1)+"_"+str(n2)) not in added_arcs:
                    add_arc_from_to(corr_places[n1], trans, net)
                    added_arcs.add((str(n1), "tr_"+str(n1)+"_"+str(n2)))
                if ("tr_"+str(n1)+"_"+str(n2), str(n2)) not in added_arcs:
                    add_arc_from_to(trans, corr_places[n2], net)
                    added_arcs.add(("tr_"+str(n1)+"_"+str(n2), str(n2)))

        for place in net.places:
            if len(place.in_arcs) < 1 and not place.name == "master_source":
                add_arc_from_to(ht_source, place, net)
            if len(place.out_arcs) < 1 and not place.name == "master_sink":
                add_arc_from_to(place, ht_sink, net)

    return net, im, fm
