from pm4py.algo.conformance.alignments import factory as align_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.mvp.projection.log import log_projection


def apply(mvp, perspective, log, net, im, fm, parameters=None):
    alignments = align_factory.apply(log, net, im, fm, parameters=parameters)

    error_occurrences = {}

    for align_trace0 in alignments:
        align_trace = align_trace0["alignment"]
        for i in range(len(align_trace)):
            move = align_trace[i]
            # search for MOVE ON MODELS involving visibile transitions
            if move[0] == ">>" and not (move[1] is None):
                j = i - 1
                while j >= 0:
                    prev_move = align_trace[j][0]
                    if not prev_move == ">>":
                        break
                    j = j - 1
                z = i + 1
                while z < len(align_trace):
                    succ_move = align_trace[z][0]
                    if not succ_move == ">>":
                        break
                    z = z + 1

                if j < 0:
                    prev_move = "START"
                if z > len(align_trace):
                    succ_move = "END"
                edge_descr = perspective + "@@" + prev_move + "@@" + move[1] + "##" + perspective + "@@" + move[
                    1] + "@@" + succ_move + "%%moveOnModel"
                if edge_descr not in error_occurrences:
                    error_occurrences[edge_descr] = 0
                error_occurrences[edge_descr] = error_occurrences[edge_descr] + 1
            if move[1] == ">>":
                z = i + 1
                while z < len(align_trace):
                    succ_move = align_trace[z][1]
                    if not (succ_move == ">>" or succ_move is None):
                        break
                    z = z + 1
                if z > len(align_trace):
                    succ_move = "END"

                j = i - 1
                while j >= 0:
                    prev_move = align_trace[j][1]
                    if not (prev_move == ">>" or prev_move is None):
                        break
                    j = j - 1
                if j < 0:
                    prev_move = "START"

                if prev_move == "START" and not succ_move == "END":
                    edge_descr = perspective + "@@" + prev_move + "%%moveOnLogStart"
                    if edge_descr not in error_occurrences:
                        error_occurrences[edge_descr] = 0
                    error_occurrences[edge_descr] = error_occurrences[edge_descr] + 1
                elif succ_move == "END":
                    edge_descr = perspective + "@@" + succ_move + "%%moveOnLogEnd"
                    if edge_descr not in error_occurrences:
                        error_occurrences[edge_descr] = 0
                    error_occurrences[edge_descr] = error_occurrences[edge_descr] + 1
                elif not (prev_move == "START" or succ_move == "END"):
                    if prev_move in mvp[perspective].nodes and succ_move in mvp[perspective].nodes:
                        edge_descr = perspective + "@@" + prev_move + "@@" + succ_move + "%%moveOnLogBothInModel"
                        if edge_descr not in error_occurrences:
                            error_occurrences[edge_descr] = 0
                        error_occurrences[edge_descr] = error_occurrences[edge_descr] + 1
                    elif prev_move in mvp[perspective].nodes:
                        edge_descr = perspective + "@@" + prev_move + "%%moveOnLogOnlyFirst"
                        if edge_descr not in error_occurrences:
                            error_occurrences[edge_descr] = 0
                        error_occurrences[edge_descr] = error_occurrences[edge_descr] + 1

    return error_occurrences


def discover_model_perspective(df, mvp, perspective, parameters=None):
    parameters_projection = {}

    parameters_projection["enable_variants_filter"] = True

    log = log_projection.apply(df, [perspective], parameters=parameters_projection)

    net, im, fm = inductive_miner.apply(log)

    return apply(mvp, perspective, log, net, im, fm, parameters=parameters)


def discover_all_models_perspectives(df, mvp, parameters=None):
    all_errors = {}

    for persp in mvp:
        all_errors.update(discover_model_perspective(df, mvp, persp, parameters=parameters))

    return all_errors