from pm4py.algo.mvp.gen_framework import factory as gen_fram_factory


class ProclDerivationModel(object):
    def __init__(self, df, parameters=None):
        if parameters is None:
            parameters = {}

        self.df = df
        self.model_dfg = gen_fram_factory.apply(df, model_type_variant="model3", rel_ev_variant="rel_dfg",
                                                node_freq_variant="type31", edge_freq_variant="type11")
        self.model_3_1 = gen_fram_factory.apply(df, model_type_variant="model3", rel_ev_variant="being_produced",
                                                node_freq_variant="type31", edge_freq_variant="type11")
        self.model_3_3 = gen_fram_factory.apply(df, model_type_variant="model3", rel_ev_variant="being_produced",
                                                node_freq_variant="type33", edge_freq_variant="type13")
        self.model_link = gen_fram_factory.apply(df, model_type_variant="model3", rel_ev_variant="link",
                                                 node_freq_variant="type31", edge_freq_variant="type11")
        self.linked_perspectives = {}

        self.find_linked_perspectives()

    def find_linked_perspectives(self):
        act_count = self.model_dfg.node_freq

        print("act_count = ",act_count)

        acti_class_map = {}

        for cl in act_count:
            for act in act_count[cl]:
                if not act in acti_class_map:
                    acti_class_map[act] = set()
                acti_class_map[act].add(cl)

        print("acti_class_map = ",acti_class_map)