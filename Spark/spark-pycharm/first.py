# Start pyspark via provided command
import pyspark
# Below code is Spark 2+
spark = pyspark.sql.SparkSession.builder.appName('test').getOrCreate()
print(spark.range(10).collect())