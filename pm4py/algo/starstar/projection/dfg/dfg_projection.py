from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics


def apply(df, perspectives_list):
    """
    Apply the projection of a StarStar dataframe to
    a DFG built following the list of perspectives

    Parameters
    ------------
    df
        Dataframe
    perspectives_list
        List of perspectives

    Returns
    -----------
    overall_dfg
        DFG obtained by merging all the perspectives
    """
    overall_dfg = {}

    for p_ind, p in enumerate(perspectives_list):
        proj_df = df[["event_id", "event_activity", p]].dropna()

        dfg_frequency = df_statistics.get_dfg_graph(proj_df, activity_key="event_activity", case_id_glue=p,
                                                    sort_timestamp_along_case_id=False)
        if len(dfg_frequency) > 0:
            for el in dfg_frequency:
                if el in overall_dfg:
                    overall_dfg[el] = max(overall_dfg[el], dfg_frequency[el])
                else:
                    overall_dfg[el] = dfg_frequency[el]

    return overall_dfg
