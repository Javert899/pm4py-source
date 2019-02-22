from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
from pm4py.objects.heuristics_net.net import HeuristicsNet


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
                heu_net = HeuristicsNet(dfg_frequency)
                heu_net.calculate()
                if len(heu_net.nodes) > 0:
                    perspectives_heu[p] = heu_net

    return perspectives_heu
