import uuid

from pm4py.objects.petri import utils
from pm4py.objects.petri.petrinet import PetriNet, Marking


def remove_unconnected_places(net):
    """
    Remove unconnected places from the Petri net

    Parameters
    -----------
    net
        Petri net

    Returns
    -----------
    net
        Petri net
    """
    places = set(net.places)
    for place in places:
        if (len(place.in_arcs) == 0) and (len(place.out_arcs) == 0):
            print("unconnected place: " + place.name)
            net.places.remove(place)
    return net


def get_initial_marking(net):
    """
    Get the initial marking from a Petri net
    (observing which nodes are without input connection)

    Parameters
    -----------
    net
        Petri net

    Returns
    -----------
    initial_marking
        Initial marking
    """
    places = set(net.places)
    initial_marking = Marking()

    for place in places:
        if len(place.in_arcs) == 0:
            initial_marking[place] = 1

    return initial_marking


def get_final_marking(net):
    """
    Get the final marking from a Petri net
    (observing which nodes are without output connection,
    if several nodes exist, then a sink place is created artificially)

    Parameters
    -------------
    net
        Petri net

    Returns
    -------------
    net
        Petri net
    final_marking
        Final marking of the Petri net
    """
    places = set(net.places)
    places_wo_output = []
    for place in places:
        if len(place.out_arcs) == 0:
            places_wo_output.append(place)

    ftranscount = 0
    final_marking = Marking()
    if len(places_wo_output) > 1:
        sink = PetriNet.Place('sink')
        net.places.add(sink)
        for place in places_wo_output:
            ftranscount = ftranscount + 1
            htrans = PetriNet.Transition("ftrans_" + str(ftranscount), None)
            net.transitions.add(htrans)
            utils.add_arc_from_to(place, htrans, net)
            utils.add_arc_from_to(htrans, sink, net)
        final_marking[sink] = 1
    elif len(places_wo_output) == 1:
        final_marking[places_wo_output[0]] = 1

    return net, final_marking


def apply(bpmn_graph, parameters=None):
    """
    Apply conversion from a BPMN graph to a Petri net
    along with an initial and final marking

    Parameters
    -----------
    bpmn_graph
        BPMN graph
    parameters
        Parameters of the algorithm

    Returns
    -----------
    net
        Petri net
    initial_marking
        Initial marking of the Petri net
    final_marking
        Final marking of the Petri net
    elements_correspondence
        Correspondence between meaningful elements of the Petri net (objects) and meaningful elements of the
        BPMN graph (dicts)
    inv_elements_correspondence
        Correspondence between meaningful elements of the BPMN graph (dicts) and meaningful elements of the
        Petri net (objects)
    el_corr_keys_map
        Correspondence between string-ed keys of elements_correspondence with the corresponding elements
    """
    if parameters is None:
        parameters = {}
    del parameters
    net = PetriNet("converted_net")
    nodes = bpmn_graph.get_nodes()
    corresponding_in_nodes = {}
    corresponding_out_nodes = {}
    elements_correspondence = {}
    inv_elements_correspondence = {}
    el_corr_keys_map = {}
    start_event_subprocess = {}
    end_event_subprocess = {}
    # adds nodes
    for node in nodes:
        node_id = node[1]['id']
        node_name = node[1]['node_name'].replace("\r", " ").replace("\n", " ").strip() if 'node_name' in node[
            1] else None
        node_type = node[1]['type'].lower()
        node_process = node[1]['process'].lower()
        trans = None
        if "task" in node_type:
            trans = PetriNet.Transition(node_id, node_name)
            net.transitions.add(trans)
            elements_correspondence[trans] = node[1]
            if not str(node[1]) in inv_elements_correspondence:
                inv_elements_correspondence[str(node[1])] = []
            inv_elements_correspondence[str(node[1])].append(trans)
        elif "gateway" in node_type:
            if "parallelgateway" in node_type:
                place = PetriNet.Place('pp_' + node_id)
                net.places.add(place)
                corresponding_in_nodes[node_id] = []
                corresponding_out_nodes[node_id] = []
                for edge in node[1]['incoming']:
                    str(edge)
                    htrans = PetriNet.Transition(str(uuid.uuid4()), None)
                    net.transitions.add(htrans)
                    hplace = PetriNet.Place(str(uuid.uuid4()))
                    net.places.add(hplace)
                    utils.add_arc_from_to(hplace, htrans, net)
                    utils.add_arc_from_to(htrans, place, net)
                    corresponding_in_nodes[node_id].append(hplace)
                for edge in node[1]['outgoing']:
                    str(edge)
                    htrans = PetriNet.Transition(str(uuid.uuid4()), None)
                    net.transitions.add(htrans)
                    hplace = PetriNet.Place(str(uuid.uuid4()))
                    net.places.add(hplace)
                    utils.add_arc_from_to(htrans, hplace, net)
                    utils.add_arc_from_to(place, htrans, net)
                    corresponding_out_nodes[node_id].append(hplace)
            else:
                input_place = PetriNet.Place('i_' + node_id)
                net.places.add(input_place)
                output_place = PetriNet.Place('o_' + node_id)
                net.places.add(output_place)
                trans = PetriNet.Transition(node_id, None)
                net.transitions.add(trans)
                utils.add_arc_from_to(input_place, trans, net)
                utils.add_arc_from_to(trans, output_place, net)
                corresponding_in_nodes[node_id] = [input_place] * len(node[1]['incoming'])
                corresponding_out_nodes[node_id] = [output_place] * len(node[1]['outgoing'])
        elif node_type == "startevent":
            source_place = PetriNet.Place(node_id)
            net.places.add(source_place)
            corresponding_in_nodes[node_id] = [source_place]
            corresponding_out_nodes[node_id] = [source_place]
            start_event_subprocess[node_process] = source_place
        elif node_type == "endevent":
            sink_place = PetriNet.Place(node_id)
            net.places.add(sink_place)
            corresponding_in_nodes[node_id] = [sink_place]
            corresponding_out_nodes[node_id] = [sink_place]
            end_event_subprocess[node_process] = sink_place
        elif "event" in node_type:
            input_place = PetriNet.Place('i_' + node_id)
            net.places.add(input_place)
            output_place = PetriNet.Place('o_' + node_id)
            net.places.add(output_place)
            trans = PetriNet.Transition(node_id, None)
            net.transitions.add(trans)
            corresponding_in_nodes[node_id] = [input_place]
            corresponding_in_nodes[node_id] = [output_place]
            utils.add_arc_from_to(input_place, trans, net)
            utils.add_arc_from_to(trans, output_place, net)
        if "task" in node_type:
            input_place = PetriNet.Place('it_' + node_id)
            net.places.add(input_place)
            output_place = PetriNet.Place('ot_' + node_id)
            net.places.add(output_place)
            corresponding_in_nodes[node_id] = [input_place]
            corresponding_out_nodes[node_id] = [output_place]
            utils.add_arc_from_to(input_place, trans, net)
            utils.add_arc_from_to(trans, output_place, net)
    # iterate again for subprocesses
    for node in nodes:
        node_id = node[1]['id']
        node_type = node[1]['type'].lower()
        node_process = node[1]['process'].lower()
        if node_type == "subprocess":
            if node_process in start_event_subprocess and node_process in end_event_subprocess:
                corresponding_in_nodes[node_id] = [start_event_subprocess[node_process]]
                corresponding_out_nodes[node_id] = [end_event_subprocess[node_process]]
    flows = bpmn_graph.get_flows()
    for flow in flows:
        flow_id = flow[2]['id']
        source_ref = flow[2]['sourceRef']
        target_ref = flow[2]['targetRef']
        if source_ref in corresponding_out_nodes and target_ref in corresponding_in_nodes and corresponding_out_nodes[
            source_ref] and corresponding_in_nodes[target_ref]:
            trans = PetriNet.Transition(flow_id, None)
            net.transitions.add(trans)
            source_arc = utils.add_arc_from_to(corresponding_out_nodes[source_ref].pop(0), trans, net)
            target_arc = utils.add_arc_from_to(trans, corresponding_in_nodes[target_ref].pop(0), net)
            elements_correspondence[target_arc] = flow
            if not str(flow) in inv_elements_correspondence:
                inv_elements_correspondence[str(flow[2])] = []
            inv_elements_correspondence[str(flow[2])].append(target_arc)
            inv_elements_correspondence[str(flow[2])].append(source_arc)

    net = remove_unconnected_places(net)
    initial_marking = get_initial_marking(net)
    net, final_marking = get_final_marking(net)

    for el in elements_correspondence:
        el_corr_keys_map[str(el)] = el

    return net, initial_marking, final_marking, elements_correspondence, inv_elements_correspondence, el_corr_keys_map
