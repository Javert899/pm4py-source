from pm4py.algo.mvp.gen_framework.models.basic_model_structure import BasicModelStructure


class MVPModel3(BasicModelStructure):
    def __init__(self, df, parameters=None):
        BasicModelStructure.__init__(self, df, parameters=parameters)
