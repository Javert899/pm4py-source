from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.other.decisiontree.applications import decision_mining_given_activities
from pm4py.objects.bpmn.exporter import bpmn20
from pm4py.objects.bpmn.util import bpmn_diagram_layouter
from pm4py.objects.conversion.log import factory as conv_factory
from pm4py.objects.conversion.petri_to_bpmn import factory as petri_to_bpmn_factory
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.visualization.bpmn.util import bpmn_embedding

SOURCE = "decmin1.csv"
TARGET = "decmin1.bpmn"
stream = csv_importer.apply(SOURCE)
log = conv_factory.apply(stream)
net, im, fm = alpha_miner.apply(log)
bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = petri_to_bpmn_factory.apply(net,
                                                                                                                 im, fm)
rules_per_edge = decision_mining_given_activities.get_rules_per_edge_given_bpmn(log, bpmn_graph)
bpmn_graph = bpmn_diagram_layouter.apply(bpmn_graph)
bpmn_graph = bpmn_embedding.embed_rules_into_bpmn(bpmn_graph, rules_per_edge)
bpmn20.export_bpmn(bpmn_graph, TARGET)
