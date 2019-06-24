import pyarrow as pa
import pyarrow.orc as orc
from pm4py.objects.log.importer.parquet import factory as parquet_importer
import time

aa = time.time()
df = parquet_importer.apply("roadtraffic.parquet")
bb = time.time()
#df = pa.Table.from_pandas(df)
#orc.write_table(df, "receipt.parquet")

cc = time.time()
data = orc.ORCFile("roadtraffic.orc")
df = data.read().to_pandas()
dd = time.time()

print(bb-aa)
print(dd-cc)
