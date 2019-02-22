from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.algo.filtering.pandas.start_activities import start_activities_filter
from pm4py.algo.filtering.pandas.end_activities import end_activities_filter
from pm4py.objects.heuristics_net.net import HeuristicsNet
from copy import copy
from pm4py.util import constants

def apply(df, parameters=None):
    """
    Discover a StarStar model from an ad-hoc built dataframe

    Parameters
    -------------
    df
        Dataframe
    parameters
        Possible parameters of the algorithm

    Returns
    -------------
    perspectives_heu
        Dictionary of perspectives associated to Heuristics Net
    """

    if parameters is None:
        parameters = {}

    perspectives_heu = {}
    perspectives = list(df.columns)
    del perspectives[perspectives.index("event_id")]
    del perspectives[perspectives.index("event_activity")]
    if "event_timestamp" in perspectives:
        del perspectives[perspectives.index("event_timestamp")]

        for p in perspectives:
            proj_df = df[["event_id", "event_activity", p]].dropna()
            dfg_frequency = df_statistics.get_dfg_graph(proj_df, activity_key="event_activity", case_id_glue=p,
                                                        sort_timestamp_along_case_id=False)

            if len(dfg_frequency) > 0:
                parameters_sa_ea = copy(parameters)
                parameters_sa_ea[constants.PARAMETER_CONSTANT_CASEID_KEY] = p
                parameters_sa_ea[constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY] = "event_activity"
                parameters_sa_ea[constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = "event_activity"
                start_activities = start_activities_filter.get_start_activities(proj_df, parameters=parameters_sa_ea)
                end_activities = end_activities_filter.get_end_activities(proj_df, parameters=parameters_sa_ea)

                heu_net = HeuristicsNet(dfg_frequency, start_activities=start_activities, end_activities=end_activities)
                heu_net.calculate()
                if len(heu_net.nodes) > 0:
                    perspectives_heu[p] = heu_net

    return perspectives_heu
