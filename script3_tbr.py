from pm4py.objects.log.importer.parquet import factory as parquet_importer
from pm4py.algo.mvp.discovery import factory as mvp_discov_factory
from pm4py.algo.mvp.places import factory as places_disc_factory
from pm4py.algo.mvp.conformance import factory as tbr_factory


df = parquet_importer.apply("tests/DATABASE_LOGS/logOpportunities.parquet")
#mvp = mvp_discov_factory.apply(df)
mvp = mvp_discov_factory.apply(df, parameters={"perspectives": ["opportunities", "campaigns", "contacts"]})
mvp, list_models = places_disc_factory.apply(df, mvp)
output = tbr_factory.apply(list_models, df)
print(output)
