from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.algo.mvp.discovery import factory as mvp_discov_factory
from pm4py.visualization.mvp import factory as mvp_vis_factory
from pm4py.algo.mvp.places import factory as places_disc_factory

df = parquet_importer.apply("tests/DATABASE_LOGS/logOpportunities.parquet")
#mvp = mvp_discov_factory.apply(df)
mvp = mvp_discov_factory.apply(df, parameters={"perspectives": ["opportunities", "campaigns", "contacts"]})
mvp, list_models = places_disc_factory.apply(df, mvp)
gviz = mvp_vis_factory.apply(mvp)
mvp_vis_factory.view(gviz)
