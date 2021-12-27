from pyspark.sql import SparkSession
from sha_helper import create_col

if __name__ == '__main__':
	spark = SparkSession.builder.appName("Testg").getOrCreate()
	df = spark.createDataFrame([(1, 'foo'), (2, 'bar')], ['id', 'name'])
	df = create_col(df)
	df.show()
