from pm4py.algo.mvp.align_model_log_on_mvp.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}
VERSIONS_DISC_MOD_PERSP = {CLASSIC: classic.discover_model_perspective}


def apply(mvp, perspective, log, net, im, fm, variant=CLASSIC, parameters=None):
    return VERSIONS[variant](perspective, log, net, im, fm)


def discover_model_perspective(df, mvp, perspective, variant=CLASSIC, parameters=None):
    return VERSIONS_DISC_MOD_PERSP[variant](df, mvp, perspective)

