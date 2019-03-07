import math
from copy import deepcopy

import numpy as np

from pm4py.objects.log.util import prefix_matrix
from pm4py.objects.petri.petrinet import PetriNet, Marking
from pm4py.objects.petri.utils import add_arc_from_to

def apply(log, parameters=None):
    if parameters is None:
        parameters = {}

    amount = 0.5j

    pref_mat, activities = prefix_matrix.get_prefix_matrix(log)
    pref_mat_array = np.asarray(pref_mat)
    v = np.asarray(np.sum(pref_mat, axis=1))

    to_keep = 1
    while to_keep < len(v):
        if v[to_keep][0] <= v[to_keep - 1][0]:
            break
        to_keep = to_keep + 1

    imaginary = np.ones((pref_mat.shape[0], pref_mat.shape[1])) * amount

    pref_mat1 = pref_mat + imaginary

    if pref_mat1.shape[0] > 501:
        pref_mat1 = pref_mat1[:500]

    P, D0, Q = np.linalg.svd(pref_mat1, full_matrices=True)

    how_many = 5
    D = np.zeros((P.shape[1], Q.shape[0]))

    for i in range(len(D0)):
        if i <= how_many:
            D[i, i] = D0[i]

    pref_mat1 = np.matmul(np.matmul(P, D), Q)
    pref_mat1_array = np.asarray(pref_mat1)
    pref_mat1_array = pref_mat1_array[:to_keep]
    pref_mat1 = np.asmatrix(pref_mat1_array)
    pref_mat1 = pref_mat1 / abs(pref_mat1).max(axis=0)
    pref_mat1_array = np.asarray(pref_mat1)
    pref_mat1_original = deepcopy(pref_mat1_array)
    i = 1
    while i < len(pref_mat1_array):
        z = 0
        while z < len(pref_mat1_array[i]):
            pref_mat1_array[i][z] = pref_mat1_original[i][z] - np.real(pref_mat1_original[i-1][z])
            z = z + 1
        i = i + 1

    i = 0
    while i < len(pref_mat1_array):
        z = 0
        maximum_real = -100000
        while z < len(pref_mat1_array[i]):
            real_value = np.real(pref_mat1_array[i][z])
            if real_value > maximum_real:
                maximum_real = real_value
            z = z + 1
        sum_values = 0
        max_ratio = 0
        z = 0
        while z < len(pref_mat1_array[i]):
            real_value = np.real(pref_mat1_array[i][z])
            if real_value > 0.75 * maximum_real:
                imaginary_value = np.imag(pref_mat1_array[i][z])
                if imaginary_value / real_value > max_ratio:
                    max_ratio = imaginary_value / real_value
                if imaginary_value > 1.7 * real_value:
                    real_value, imaginary_value = real_value / math.sqrt(
                        real_value * real_value + imaginary_value * imaginary_value), imaginary_value / math.sqrt(
                        real_value * real_value + imaginary_value * imaginary_value)
                    pref_mat1_array[i][z] = real_value * (real_value + imaginary_value * 1.0j)
                else:
                    pref_mat1_array[i][z] = real_value
                sum_values = sum_values + real_value
            else:
                pref_mat1_array[i][z] = 0
            z = z + 1
        #print(max_ratio)
        z = 0
        while z < len(pref_mat1_array[i]):
            pref_mat1_array[i][z] = pref_mat1_array[i][z] / sum_values
            z = z + 1
        i = i + 1

    net = PetriNet("net")
    im = Marking()
    fm = Marking()
    source = PetriNet.Place("source")
    sink = PetriNet.Place("sink")
    net.places.add(source)
    net.places.add(sink)
    im[source] = 1
    fm[sink] = 1

    count_trans = 0
    prev_place = source
    i = 0
    while i < len(pref_mat1_array):
        added_in_this_step = []
        added_skip = False
        z = 0
        while z < len(pref_mat1_array[i]):
            if np.real(pref_mat1_array[i][z]) > 0:
                if np.imag(pref_mat1_array[i][z]) > 0:
                    if not added_skip:
                        count_trans = count_trans + 1
                        skip_trans = PetriNet.Transition("tr_"+str(count_trans), None)
                        net.transitions.add(skip_trans)
                        added_in_this_step.append(skip_trans)
                        add_arc_from_to(prev_place, skip_trans, net)
                        added_skip = True
                count_trans = count_trans + 1
                this_trans = PetriNet.Transition("tr_"+str(count_trans), activities[z])
                net.transitions.add(this_trans)
                added_in_this_step.append(this_trans)
                add_arc_from_to(prev_place, this_trans, net)
            z = z + 1
        if i == len(pref_mat1_array)-1:
            prev_place = sink
        else:
            prev_place = PetriNet.Place("target_"+str(i))
            net.places.add(prev_place)

        for trans in added_in_this_step:
            add_arc_from_to(trans, prev_place, net)

        i = i + 1

    return net, im, fm
