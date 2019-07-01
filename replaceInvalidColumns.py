from pm4py.objects.log.importer.parquet import factory as parquet_importer
import re
from pm4py.objects.log.exporter.parquet import factory as parquet_exporter

FILE = "Billing.parquet"
df = parquet_importer.apply(FILE)
df.columns = [re.sub('[^0-9a-zA-Z]+', '', y.replace(':','AJIWEIO')).replace('AJIWEIO',':') for y in df.columns]
print(df.columns)
parquet_exporter.apply(df, FILE)
