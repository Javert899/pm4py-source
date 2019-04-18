from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.conversion.log import factory as conv_factory


stream = csv_importer.apply("conceptdrift1.csv")
log = conv_factory.apply(stream)

from pm4py.algo.other.conceptdrift import factory as concept_drift_factory
drift_found, logs_list, endpoints, change_date_repr = concept_drift_factory.apply(log)

print(drift_found)
print(logs_list)
print(endpoints)
print(change_date_repr)