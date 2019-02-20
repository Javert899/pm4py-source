import os

from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.objects.conversion.petri_to_bpmn import factory as petri_to_bpmn_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.visualization.bpmn import factory as bpmn_vis_factory
from pm4py.visualization.bpmn.util import convert_performance_map
from pm4py.visualization.petrinet.util.vis_trans_shortest_paths import get_decorations_from_dfg_spaths_acticount
from pm4py.visualization.petrinet.util.vis_trans_shortest_paths import get_shortest_paths


def execute_script():
    # load the dataframe
    dataframe = csv_import_adapter.import_dataframe_from_path(
        os.path.join("..", "tests", "input_data", "running-example.csv"))
    # count the number of occurrences for each activity
    activities_count = attributes_filter.get_attribute_values(dataframe, "concept:name")
    # calculate DFGs
    [dfg_frequency, dfg_performance] = df_statistics.get_dfg_graph(dataframe, measure="both",
                                                                   perf_aggregation_key="median")
    # apply Inductive Miner
    net, initial_marking, final_marking = inductive_miner.apply_dfg(dfg_frequency)
    # calculate shortest paths on the Petri net
    spaths = get_shortest_paths(net)
    # calculate aggregated statistics from spaths, DFGs and activities count
    aggr_stat_frequency = get_decorations_from_dfg_spaths_acticount(net, dfg_frequency,
                                                                    spaths,
                                                                    activities_count,
                                                                    variant="frequency")
    aggr_stat_performance = get_decorations_from_dfg_spaths_acticount(net, dfg_performance,
                                                                      spaths,
                                                                      activities_count,
                                                                      variant="performance")
    # convert the Petri net into a BPMN diagram
    bpmn_diagram, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = petri_to_bpmn_factory.apply(
        net, initial_marking, final_marking)
    bpmn_stat_frequency = convert_performance_map.convert_performance_map_to_bpmn(aggr_stat_frequency,
                                                                                  inv_elements_correspondence)
    bpmn_stat_performance = convert_performance_map.convert_performance_map_to_bpmn(aggr_stat_performance,
                                                                                  inv_elements_correspondence)
    # obtain and display frequency GVIZ representation of the BPMN through back-conversion to Petri
    gviz = bpmn_vis_factory.apply(bpmn_diagram, bpmn_stat_frequency, variant="frequency", parameters={"format": "svg"})
    bpmn_vis_factory.view(gviz)
    # obtain and display performance GVIZ representation of the BPMN through back-conversion to Petri
    gviz = bpmn_vis_factory.apply(bpmn_diagram, bpmn_stat_performance, variant="performance", parameters={"format": "svg"})
    bpmn_vis_factory.view(gviz)


if __name__ == "__main__":
    execute_script()
