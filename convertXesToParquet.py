from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter

log = xes_importer.apply("roadtraffic.xes.gz")
parquet_exporter.apply(log, "roadtraffic.parquet")
