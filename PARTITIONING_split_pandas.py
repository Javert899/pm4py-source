from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter

df = parquet_importer.apply("C:\\bpic2018.parquet")
parquet_exporter.apply(df, "bpic2018", parameters={"auto_partitioning": True, "num_partitions": 64})
