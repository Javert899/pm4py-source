from pm4py.algo.conformance.alignments import factory as align_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.algo.mvp.projection.log import log_projection


def apply(perspective, log, net, im, fm, parameters=None):
    alignments = align_factory.apply(log, net, im, fm, parameters=parameters)

    error_occurrences = {}

    for align_trace0 in alignments:
        align_trace = align_trace0["alignment"]
        passed_start = False
        for i in range(len(align_trace)):
            move = align_trace[i]
            if not (move[1] == ">>" or move[1] is None):
                print("passed_start", move)
                passed_start = True
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
                    if not succ_move == ">>":
                        break
                    z = z + 1
                if z > len(align_trace):
                    succ_move = "END"
                
                if not passed_start and not succ_move == "END":
                    edge_descr = perspective + "@@START@@" + succ_move + "%%moveOnLogStart"
                    if edge_descr not in error_occurrences:
                        error_occurrences[edge_descr] = 0
                    error_occurrences[edge_descr] = error_occurrences[edge_descr] + 1

    print(error_occurrences)


def discover_model_perspective(df, mvp, perspective, parameters=None):
    parameters_projection = {}

    parameters_projection["enable_variants_filter"] = True

    log = log_projection.apply(df, [perspective], parameters=parameters_projection)

    net, im, fm = inductive_miner.apply(log)

    return apply(perspective, log, net, im, fm, parameters=parameters)
