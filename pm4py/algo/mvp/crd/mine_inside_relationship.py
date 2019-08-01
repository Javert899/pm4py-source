from pm4py.algo.mvp.crd import get_first_for_object, get_last_for_object
from pm4py.objects.heuristics_net import defaults
import math
import numpy as np


def apply(df, parameters=None):
    if parameters is None:
        parameters = {}

    consumers = parameters["consumers"] if "consumers" in parameters else None

    cols = [x for x in df.columns if not x.startswith("event_")]

    temp_ports = {}
    ports = {}

    for iii, col in enumerate(cols):
        if consumers is None or col in consumers["consumer_per_class"]:
            df0 = df.dropna(how='any', subset=[col])
            i1 = df.set_index("event_id").index
            i2 = df0.set_index("event_id").index

            red_df = df[i1.isin(i2)]

            for jjj, c2 in enumerate(cols):
                if not col == c2:
                    if consumers is None or c2 in consumers["consumer_per_class"][col]:
                        print("mining_ports",col,c2,iii,len(cols),jjj,len(cols))
                        first_df = red_df.groupby(c2).first()
                        second_df = red_df.groupby(c2).last()
                        red_df_col_not_null = red_df.dropna(how='any', subset=[col])
                        i1 = red_df_col_not_null.set_index("event_id").index
                        i2 = first_df.set_index("event_id").index
                        i3 = second_df.set_index("event_id").index

                        first_df = red_df_col_not_null[i1.isin(i2)]
                        second_df = red_df_col_not_null[~i1.isin(i2)]

                        first_acti_count = dict(first_df["event_activity"].value_counts())
                        second_acti_count = dict(second_df["event_activity"].value_counts())

                        second_df.columns = [x + "_2" for x in second_df.columns]

                        joined_df = first_df.merge(second_df, left_on=[col, c2], right_on=[col + "_2", c2 + "_2"],
                                                   suffixes=('', ''))

                        rel_count = dict(joined_df.groupby(["event_activity", "event_activity_2"]).size())

                        print(col, c2, rel_count)

                        for couple in rel_count:
                            act1 = couple[0]
                            act2 = couple[1]

                            if act1 in first_acti_count and act2 in second_acti_count:
                                print(col, c2, act1, act2)
                                if col not in temp_ports:
                                    temp_ports[col] = {}
                                if c2 not in temp_ports[col]:
                                    temp_ports[col][c2] = {}
                                if act2 not in temp_ports[col][c2]:
                                    temp_ports[col][c2][act2] = {}

                                temp_ports[col][c2][act2][act1] = [rel_count[couple], first_acti_count[act1],
                                                                   second_acti_count[act2]]

        for col in temp_ports:
            for c2 in temp_ports[col]:
                for act2 in temp_ports[col][c2]:
                    if temp_ports[col][c2][act2]:
                        all_keys = list(temp_ports[col][c2][act2].keys())
                        summ = np.sum([x[0] for x in temp_ports[col][c2][act2].values()])
                        if summ == temp_ports[col][c2][act2][all_keys[0]][2] or True:
                            if not col in ports:
                                ports[col] = {}
                            if not c2 in ports[col]:
                                ports[col][c2] = {}
                            if not act2 in ports[col][c2]:
                                ports[col][c2][act2] = {}

                            for act in temp_ports[col][c2][act2]:
                                if temp_ports[col][c2][act2][act][0] == temp_ports[col][c2][act2][act][1]:
                                    ports[col][c2][act2][act] = "="
                                else:
                                    ports[col][c2][act2][act] = "<="

                            bool_vect = [x[0] == x[1] for x in temp_ports[col][c2][act2].values()]
                            res = True
                            for v in bool_vect:
                                res = res and v
                            if res:
                                ports[col][c2][act2]["@@complex"] = "="
                            else:
                                ports[col][c2][act2]["@@complex"] = "<="


    return ports
