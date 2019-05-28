from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.objects.xoc.importer import factory as xoc_importer
import pandas as pd
from pm4py.algo.mvp.n2v_encoding import encode
import joblib
from pm4py.algo.mvp.n2v_encoding.concept_drift import drift
import random
from pm4py.objects.xoc.exporter import factory as xoc_exporter


df1 = xoc_importer.apply("tests//DATABASE_LOGS//log.xoc")
df2 = parquet_importer.apply("tests//DATABASE_LOGS//logOpportunities.parquet")

all_events_df1 = list(set(df1["event_id"]))
all_events_df2 = list(set(df2["event_id"]))
random.shuffle(all_events_df1)
random.shuffle(all_events_df2)

all_events_df2 = all_events_df2[:len(all_events_df1)]
df2 = df2[df2["event_id"].isin(all_events_df2)]

xoc_exporter.apply(df2, "opportunities_red.xoc")

df3 = pd.concat([df1, df2])

encoding = encode.from_df(df3)

joblib.dump(encoding, "n2v_mixedLO.dump", compress=3)

encoding = joblib.load("n2v_mixedLO.dump")

parameters = {}
parameters["encoding"] = encoding

drifted_logs = drift.apply(df3, parameters=parameters)

for index, log in enumerate(drifted_logs):
    xoc_exporter.apply(log, "drift_"+str(index)+".xoc")

print(len(drifted_logs))