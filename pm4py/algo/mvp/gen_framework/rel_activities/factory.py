from pm4py.algo.mvp.gen_framework.rel_activities import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(df, rel_ev_dict, variant=CLASSIC, parameters=None):
    if parameters is None:
        parameters = {}

    return VERSIONS[variant](df, rel_ev_dict, parameters=parameters)
