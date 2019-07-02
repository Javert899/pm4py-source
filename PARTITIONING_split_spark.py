from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, LongType
from pyspark.sql.functions import udf

def ggg(x):
	return abs(hash(x)) % (64)

ggg2 = udf(ggg, LongType())

# initialise sparkContext
spark = SparkSession.builder \
    .master('local') \
    .appName('myAppName') \
    .config('spark.executor.memory', '5gb') \
    .config("spark.cores.max", "6") \
    .getOrCreate()
sc = spark.sparkContext

# using SQLContext to read parquet file
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# to read parquet file
df = sqlContext.read.parquet('bpic2017.parquet')
df2 = df.withColumn("@@partitioning", ggg2("caseAAAconceptAAAname"))
#df2 = df.withColumn("@@partitioning",df["caseAAAconceptAAAname"].cast(IntegerType()))
#df2.select("@@partitioning").show()

#df.select(g2("caseAAAconceptAAAname")).take(2)
#df2 = df.withColumn("@@partitioning", g("caseAAAconceptAAAname"))
#df2.select("@@partitioning").show()
#input()
df2.write.partitionBy("@@partitioning").parquet("b2017")

#df.write.format("orc").save("Billing.orc")
