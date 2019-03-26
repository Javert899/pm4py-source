from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.algo.discovery.massive_places import factory as massive_places_factory
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.evaluation.replay_fitness import factory as replay_fitness_factory
from pm4py.objects.log.util import prefix_matrix
import time


aa = time.time()
log = xes_importer.apply("C:\\receipt.xes", variant="nonstandard")
bb = time.time()
print("time to import the model: ",(bb-aa))
net, im, fm = massive_places_factory.apply(log)
cc = time.time()
print("time to calculate the model ",(cc-bb))
gviz = pn_vis_factory.apply(net, im, fm)
pn_vis_factory.view(gviz)
fitness = replay_fitness_factory.apply(log, net, im, fm)
print(fitness)
pref_mat, var_mat, activities = prefix_matrix.get_prefix_variants_matrix(log)

print(var_mat)
print(var_mat.shape)
print(pref_mat)
print(pref_mat.shape)