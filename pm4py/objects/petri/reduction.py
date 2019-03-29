from pm4py.objects.petri.utils import remove_transition, remove_place, add_arc_from_to


def reduce1(net):
    """
    Reduction rule (1) to simplify the Petri net

    Parameters
    ------------
    net
        Petri net

    Returns
    ------------
    net
        Simplified Petri net
    """
    something_changed = True
    while something_changed:
        something_changed = False
        transitions = list(net.transitions)
        for trans in transitions:
            source_places = [arc.source for arc in trans.in_arcs]
            target_places = [arc.target for arc in trans.out_arcs]
            target_transes = [arc.target for place in target_places for arc in place.out_arcs]
            if len(source_places) == 1 and len(target_places) == 1 and len(target_transes) == 1:
                source_place = source_places[0]
                target_place = target_places[0]
                target_trans = target_transes[0]
                #target_places2 = [arc.target for arc in target_trans.out_arcs]
                if len(target_place.in_arcs) == 1 and len(target_trans.in_arcs) == 1 and len(
                        target_trans.out_arcs) == 1:
                    if trans.label is None:
                        net = remove_transition(net, trans)
                        net = remove_place(net, target_place)
                        add_arc_from_to(source_place, target_trans, net)
                        something_changed = True
                        continue
    return net


def reduce(net):
    """
    Reduction rule to simplify the Petri net

    Parameters
    -------------
    net
        Petri net

    Returns
    -------------
    net
        Simplified Petri net
    """
    return reduce1(net)
