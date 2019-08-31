import pandas as pd
from pm4py.util import constants
from pm4py.algo.filtering.common.filtering_constants import CASE_CONCEPT_NAME
from pm4py.objects.log.util import xes
from pm4py.algo.discovery.dfg.predictor import DFGPredictor


def apply(dataframe, dfg, parameters=None):
    if parameters is None:
        parameters = {}

    case_id_glue = parameters[
        constants.PARAMETER_CONSTANT_CASEID_KEY] if constants.PARAMETER_CONSTANT_CASEID_KEY in parameters else CASE_CONCEPT_NAME
    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY

    dfg_predictor = DFGPredictor(dfg)

    shifted_df = dataframe.shift(-1)[[case_id_glue, activity_key]]
    shifted_df.columns = [x+"_2" for x in shifted_df]
    concat_df = pd.concat([dataframe, shifted_df], axis=1)
    concat_df = concat_df[concat_df[case_id_glue] == concat_df[case_id_glue+"_2"]]
    concat_df["@@merged_activities"] = concat_df[activity_key]+"@@"+concat_df[activity_key+"_2"]
    concat_df_red = concat_df["@@merged_activities"]
    all_paths = concat_df_red.unique()
    replace_dict = dfg_predictor.merged_dict
    for path in all_paths:
        if path not in replace_dict:
            replace_dict[path] = 0.0
    concat_df_red = concat_df_red.replace(replace_dict)
    concat_df["@@fp_couple_fitness"] = concat_df_red

    return concat_df
