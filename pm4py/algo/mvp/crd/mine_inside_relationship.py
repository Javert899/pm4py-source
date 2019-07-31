from pm4py.algo.mvp.crd import get_first_for_object, get_last_for_object
from pm4py.objects.heuristics_net import defaults
import math


def mine_inside_relationship(df, parameters=None):
    if parameters is None:
        parameters = {}

    cols = [x for x in df.columns if not x.startswith("event_")]

    for iii, col in enumerate(cols):
        df0 = df.dropna(how='any', subset=[col])
        i1 = df.set_index("event_id").index
        i2 = df0.set_index("event_id").index

        red_df = df[i1.isin(i2)].reset_index()

        for jjj, c2 in enumerate(cols):
            first_df = red_df.groupby(c2).first()
            second_df = red_df.groupby(c2).last()

            red_df_col_not_null = red_df.dropna(how='any', subset=[col])
            i1 = red_df_col_not_null.set_index("event_id").index
            i2 = first_df.set_index("event_id").index
            i3 = second_df.set_index("event_id").index

            first_df = red_df_col_not_null[i1.isin(i2)].reset_index()
            second_df = red_df_col_not_null[i1.isin(i3)].reset_index()

            print(len(first_df), len(second_df))

        #print(len(df), len(red_df))