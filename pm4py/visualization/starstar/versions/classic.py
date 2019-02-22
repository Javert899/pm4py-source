from pm4py.visualization.heuristics_net.versions import pydotplus as heu_visualizer


def apply(model, parameters=None):
    if parameters is None:
        parameters = {}

    overall_heu = None
    for persp_name in model:
        persp = model[persp_name]
        if overall_heu is None:
            overall_heu = persp
        else:
            overall_heu = overall_heu + persp
    return heu_visualizer.apply(overall_heu, parameters=parameters)
