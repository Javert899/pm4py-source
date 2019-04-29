from pm4py.algo.mvp.align_model_log_on_mvp.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}
VERSIONS_DISC_MOD_PERSP = {CLASSIC: classic.discover_model_perspective}
VERSIONS_ALL_MODELS = {CLASSIC: classic.discover_all_models_perspectives}

def apply(mvp, perspective, log, net, im, fm, variant=CLASSIC, parameters=None):
    return VERSIONS[variant](perspective, log, net, im, fm, parameters=parameters)


def discover_model_perspective(df, mvp, perspective, variant=CLASSIC, parameters=None):
    return VERSIONS_DISC_MOD_PERSP[variant](df, mvp, perspective, parameters=parameters)


def discover_all_models_perspectives(df, mvp, variant=CLASSIC, parameters=None):
    return VERSIONS_ALL_MODELS[variant](df, mvp, parameters=parameters)
