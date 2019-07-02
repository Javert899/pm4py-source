from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.algo.discovery.dfg.adapters.pandas import df_statistics
import time
from collections import Counter
import gc

aa = time.time()
df = parquet_importer.apply("C:\\bpic2018.parquet", parameters={"columns": ["case:concept:name", "concept:name"]})
dfg = Counter(df_statistics.get_dfg_graph(df, sort_caseid_required=False, sort_timestamp_along_case_id=False))
#print(dfg)
bb = time.time()
print("time to import a single Parquet file and calculate the directly-follows graph",(bb-aa))
del df
gc.collect()
print("garbage collected, start again")
aa = time.time()
overall_dfg = Counter()
all_parquets = parquet_importer.get_list_parquet("bpic2018")
for parq in all_parquets:
    df = parquet_importer.apply(parq, parameters={"columns": ["case:concept:name", "concept:name"]})
    this_dfg = Counter(df_statistics.get_dfg_graph(df, sort_caseid_required=False, sort_timestamp_along_case_id=False))
    overall_dfg = overall_dfg + this_dfg
bb = time.time()
print("time to import ALL the corresponding Parquet files and calculate the directly-follows graph",(bb-aa))
#print(overall_dfg)