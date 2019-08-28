from pm4py.algo.mvp.gen_framework.models import model1

MODEL1 = "model1"

VERSIONS = {MODEL1: model1.MVPModel1}


def apply(df, variant=MODEL1, parameters=None):
    return VERSIONS[variant](df, parameters=parameters)
