import os
import unittest

from pm4py.algo.other.decisiontree.applications import root_cause_part_duration, decision_mining_given_activities
from pm4py.objects.bpmn.exporter import bpmn20 as bpmn_exporter
from pm4py.objects.bpmn.importer import bpmn20 as bpmn_importer
from pm4py.objects.conversion.bpmn_to_petri import factory as bpmn_to_petri
from pm4py.objects.conversion.petri_to_bpmn import factory as petri_to_bpmn
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.petri.importer import pnml as petri_importer
from pm4py.visualization.bpmn import factory as bpmn_vis_factory
from tests.constants import INPUT_DATA_DIR, OUTPUT_DATA_DIR
from pm4py.visualization.bpmn.util import bpmn_embedding
from pm4py.algo.discovery.inductive import factory as inductive_miner

class BpmnTests(unittest.TestCase):
    def test_bpmn_conversion_to_petri(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        net, initial_marking, final_marking, el_corr, inv_el_corr, el_corr_keys_map = bpmn_to_petri.apply(
            bpmn_graph)
        del net
        del initial_marking
        del final_marking
        del el_corr
        del inv_el_corr
        del el_corr_keys_map

    def test_petri_conversion_to_bpmn(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.pnml")
        net, initial_marking, final_marking = petri_importer.import_net(obj_path)
        bpmn_graph, el_corr, inv_el_corr, el_corr_keys_map = petri_to_bpmn.apply(net,
                                                                                 initial_marking,
                                                                                 final_marking)
        del bpmn_graph
        del el_corr
        del inv_el_corr
        del el_corr_keys_map

    def test_bpmn_exporting(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        output_path = os.path.join(OUTPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        bpmn_exporter.export_bpmn(bpmn_graph, output_path)
        os.remove(output_path)

    def test_bpmn_simple_vis(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        gviz = bpmn_vis_factory.apply(bpmn_graph, parameters={"format": "svg"})
        del gviz

    def test_bpmn_freqperf_vis_conv(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        log = xes_importer.apply(os.path.join(INPUT_DATA_DIR, "running-example.xes"))
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        gviz = bpmn_vis_factory.apply_through_conv(bpmn_graph, log=log, variant="frequency")
        del gviz
        gviz = bpmn_vis_factory.apply_through_conv(bpmn_graph, log=log, variant="performance")
        del gviz

    def test_bpmn_embedding(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        log = xes_importer.apply(os.path.join(INPUT_DATA_DIR, "running-example.xes"))
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        bpmn_graph = bpmn_vis_factory.apply_embedding(bpmn_graph, log=log, variant="frequency")
        bpmn_graph = bpmn_vis_factory.apply_embedding(bpmn_graph, log=log, variant="performance")
        bpmn_exporter.export_bpmn(bpmn_graph, os.path.join(OUTPUT_DATA_DIR, "running-example.bpmn"))

    def test_bpmn_root_cause(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        log = xes_importer.apply(os.path.join(INPUT_DATA_DIR, "running-example.xes"))
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        clf, feature_names, classes = root_cause_part_duration.perform_duration_root_cause_analysis_given_bpmn(log,
                                                                                                               bpmn_graph,
                                                                                                               "decide")


    def test_bpmn_decision_mining_on_activities(self):
        # to avoid static method warnings in tests,
        # that by construction of the unittest package have to be expressed in such way
        self.dummy_variable = "dummy_value"
        log = xes_importer.apply(os.path.join(INPUT_DATA_DIR, "receipt.xes"))
        net, initial_marking, final_marking = inductive_miner.apply(log)
        bpmn_graph, el_corr, inv_el_corr, el_corr_keys_map = petri_to_bpmn.apply(net,
                                                                                 initial_marking,
                                                                                 final_marking)

        rules_per_edge = decision_mining_given_activities.get_rules_per_edge_given_bpmn(log, bpmn_graph)
        bpmn_graph = bpmn_embedding.embed_rules_into_bpmn(bpmn_graph, rules_per_edge)

if __name__ == "__main__":
    unittest.main()
