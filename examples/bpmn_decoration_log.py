import os

from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.conversion.petri_to_bpmn import factory as petri_to_bpmn_factory
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.visualization.bpmn import factory as bpmn_vis_factory


def execute_script():
    # import log
    log = xes_importer.apply(os.path.join("..", "tests", "input_data", "running-example.xes"))
    # calculate Petri net through Inductive Miner
    net, initial_marking, final_marking = inductive_miner.apply(log)
    # convert the Petri net into a BPMN diagram
    bpmn_diagram, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = petri_to_bpmn_factory.apply(
        net, initial_marking, final_marking)
    # obtain and display frequency GVIZ representation of the BPMN through back-conversion to Petri
    gviz = bpmn_vis_factory.apply_through_conv(bpmn_diagram, log=log, variant="frequency", parameters={"format": "svg"})
    bpmn_vis_factory.view(gviz)
    # obtain and display performance GVIZ representation of the BPMN through back-conversion to Petri
    gviz = bpmn_vis_factory.apply_through_conv(bpmn_diagram, log=log, variant="performance", parameters={"format": "svg"})
    bpmn_vis_factory.view(gviz)
    # annotate the BPMN
    bpmn_diagram = bpmn_vis_factory.apply_embedding(bpmn_diagram, log=log, variant="frequency")
    bpmn_diagram = bpmn_vis_factory.apply_embedding(bpmn_diagram, log=log, variant="performance")


if __name__ == "__main__":
    execute_script()
