from pm4py.objects.log.util import xes
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri.utils import add_arc_from_to
from pm4py.util import constants
from scipy.linalg import null_space
from pm4py.objects.log.util import prefix_matrix
import numpy as np


MAX_NO_PLACES_EVALUATED = "max_no_places_evaluated"


def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    net = PetriNet("net")
    im = Marking()
    fm = Marking()
    pcount = 0

    activity_key = parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] if constants.PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else xes.DEFAULT_NAME_KEY
    max_no_places_evaluated = parameters[MAX_NO_PLACES_EVALUATED] if MAX_NO_PLACES_EVALUATED in parameters else 1000
    thresh1 = 0.6
    thresh2 = 0.000001
    parameters[
        constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = activity_key
    parameters[constants.PARAMETER_CONSTANT_ATTRIBUTE_KEY] = activity_key
    compl_var_repr, par_var_repr, feature_names = prefix_matrix.get_prefix_variants_matrix(log, parameters)
    dict_trans = {}
    for act in feature_names:
        dict_trans[act] = PetriNet.Transition(act, act)
        net.transitions.add(dict_trans[act])
    ns = null_space(par_var_repr)
    rand_mat = 2*np.random.rand(ns.shape[1], max_no_places_evaluated)-1
    rand_mat = rand_mat / abs(rand_mat).sum(axis=0)
    right_mat = np.matmul(ns, rand_mat)
    right_mat = right_mat / abs(rand_mat).max(axis=0)
    right_mat[right_mat <= -thresh1] = -1
    right_mat[right_mat >= thresh1] = 1
    right_mat[abs(right_mat) < thresh1] = 0
    right_mat = np.unique(right_mat, axis=1)
    check_mat = np.matmul(par_var_repr, right_mat)
    check_mat_sum_col = list(check_mat.sum(axis=0))
    zero_indexes = []
    i = 0
    while i < len(check_mat_sum_col):
        if check_mat_sum_col[i] == 0:
            zero_indexes.append(i)
        i = i + 1
    right_mat = right_mat[:, zero_indexes]
    final_mat = np.matmul(compl_var_repr, right_mat)
    final_mat[final_mat < 0] = 0
    colsum = list(final_mat.sum(axis=0))
    i = 0
    while i < len(colsum):
        if colsum[i] < thresh2:
            vec = list(right_mat[:, i])
            preset = []
            postset = []
            if max(vec) > 0:
                j = 0
                while j < len(vec):
                    if vec[j] < 0:
                        act = feature_names[j]
                        preset.append(act)
                    elif vec[j] > 0:
                        act = feature_names[j]
                        postset.append(act)
                    j = j + 1
                if len(preset) > 0 and len(postset) > 0:
                    pcount = pcount + 1
                    place = PetriNet.Place("p_"+str(pcount))
                    net.places.add(place)
                    for act in preset:
                        add_arc_from_to(dict_trans[act], place, net)
                    for act in postset:
                        add_arc_from_to(place, dict_trans[act], net)
        i = i + 1
    return net, im, fm
