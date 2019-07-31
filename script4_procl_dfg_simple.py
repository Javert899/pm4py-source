from pm4py.objects.xoc.importer import factory as xoc_importer
from pm4py.algo.mvp.general_pcl_dfg import get_object
from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.visualization.mvp.clustered_pcl_dfg import visualizer
from pm4py.algo.mvp.crd import mine_inside_relationship

df = parquet_importer.apply("tests/DATABASE_LOGS/opp_commercial.parquet")
columns = ["opportunities", "leads", "contacts"]
all_columns = columns + ["event_id", "event_activity", "event_timestamp"]
df = df[all_columns].dropna(how='all', subset=columns)
obj = get_object.apply(df)
gviz = visualizer.apply(obj, parameters={"format": "svg"})
visualizer.view(gviz)
