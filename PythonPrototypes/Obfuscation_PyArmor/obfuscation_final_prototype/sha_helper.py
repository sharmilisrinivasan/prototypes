from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StructField, StructType, StringType

def get_schema(data_df):
    return StructType(data_df.schema.fields +
                      [StructField("new_field", StringType(), True)])

def lambda_method(my_schema, custom_val):
	@pandas_udf(my_schema, PandasUDFType.GROUPED_MAP)
	def lambda_udf(group_df):
		group_df["new_field"] = group_df.apply(lambda x: "Hello"+ x["name"] + custom_val, axis=1)
		return group_df
	return lambda_udf

def create_col(data_df):
	my_udf = lambda_method(get_schema(data_df), "I am custom Val")
	return data_df.groupBy("id").apply(my_udf)
