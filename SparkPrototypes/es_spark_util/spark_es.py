from typing import List, Union

from pyspark.sql import DataFrame
from pyspark.sql.readwriter import DataFrameReader, DataFrameWriter
from pyspark.sql.session import SparkSession


class SparkESConstants:
    DEFAULT_SAVE_MODE = "append"
    ES_JAR = "elasticsearch-spark"
    ES_JAR_EXCEPTION_MSG = \
        "Spark session does not have suitable ES connector jar added - Add and retry"
    ES_KEY_DF_WRITE_NULL = "es.spark.dataframe.write.null"
    ES_KEY_JARS = "spark.jars"
    ES_KEY_MAPPING_ID = "es.mapping.id"
    ES_KEY_NODES = "es.nodes"
    ES_KEY_OPTION_QUERY = "es.query"
    ES_KEY_PORT = "es.port"
    ES_KEY_WRITE_OP = "es.write.operation"
    ES_SET_DF_WRITE_NULL = "true"
    ES_URL_CONJ = ":"
    FORMAT = "org.elasticsearch.spark.sql"


class SparkESConnector:
    """
    PySpark-Elastic connector wrapper

    :ivar str elastic_ip: IP of the Elastic to be connected
    :ivar str elastic_port: Port of the Elastic to be connected
    :ivar SparkSession spark: Session to used in read and write operations
    """
    def __init__(self, spark_session_: SparkSession, elastic_url: str) -> None:
        """
        Checks for required spark-es jar in Spark session and initialises instance variable.
        Raises Exception otherwise

        :param spark_session_: Session to used in read and write operations
        :type spark_session_: SparkSession
        :param elastic_url: Elastic URL string used to establish elastic connection
        :type elastic_url: str
        """
        self.elastic_ip, self.elastic_port = \
            self._get_elastic_ip_port(elastic_url)
        spark_jar_conf = spark_session_.sparkContext.getConf().get(
            SparkESConstants.ES_KEY_JARS)
        if spark_jar_conf and SparkESConstants.ES_JAR in spark_jar_conf:
            self.spark = spark_session_
        else:
            raise Exception(SparkESConstants.ES_JAR_EXCEPTION_MSG)

    @staticmethod
    def _add_es_attributes(read_writer: Union[DataFrameReader,
                                              DataFrameWriter],
                           elastic_ip: str, es_port: str) -> Union[DataFrameReader,
                                                                   DataFrameWriter]:
        """
        Adds ES related options to Reader/Writer object

        :param read_writer: Reader/Writer object to be updated
        :type read_writer: DataFrameReader/ DataFrameWriter
        :param elastic_ip: IP of the Elastic to be connected
        :type elastic_ip: str
        :param es_port: Port of the Elastic to be connected
        :type es_port: str

        :return: Updated Reader/Writer object
        :rtype: DataFrameReader/ DataFrameWriter
        """
        return (read_writer.
                format(SparkESConstants.FORMAT).
                option(SparkESConstants.ES_KEY_NODES, elastic_ip).
                option(SparkESConstants.ES_KEY_PORT, es_port).
                option(SparkESConstants.ES_KEY_DF_WRITE_NULL,
                       SparkESConstants.ES_SET_DF_WRITE_NULL))

    @staticmethod
    def _get_elastic_ip_port(elastic_url: str):
        """

        :param elastic_url: Elastic URL string used to establish elastic connection
        :type elastic_url: str

        :return: Parses and returns Elastic IP and port from the Elastic URL
        :rtype: str, str
        """
        if not elastic_url:
            return None, None
        elastic_parts = elastic_url.split(SparkESConstants.ES_URL_CONJ)
        return elastic_parts[0], elastic_parts[1]

    def read_index(self, index_: str, query_: str = None,
                   fields: List[str] = None,
                   renames_: List[str] = None) -> DataFrame:
        """
        Reads data from ES and returns in the form of Spark DataFrame

        :param index_: ES mapping index to be read
        :type index_: str
        :param query_: Query (filters) to be used on ES read
        :type query_: str
        :param fields: Set of fields to be read from ES
        :type fields: List[str]
        :param renames_: One-on-one mapping with fields, if they are to be renamed
        :type renames_: List[str]

        :return: Data read from ES into Spark DataFrame
        :rtype: DataFrame
        """
        to_return = self._add_es_attributes(self.spark.read, self.elastic_ip, self.elastic_port)
        if query_:
            to_return = to_return.option(SparkESConstants.ES_KEY_OPTION_QUERY, query_)
        to_return = to_return.load(index_)
        if fields:
            to_return = to_return.select(fields)
        if renames_:
            to_return = to_return.toDF(*renames_)
        return to_return

    def write_index(self, index_: str, df_: DataFrame,
                    save_mode_: str = SparkESConstants.DEFAULT_SAVE_MODE,
                    renames_: List[str] = None,
                    write_op_: str = None,
                    mapping_id_: str = None) -> None:
        """

        :param index_: ES mapping index to be written to
        :type index_: str
        :param df_: Data to be written to ES
        :type df_: DataFrame
        :param save_mode_: Mode of writing to ES index - Overwrite / Append
        :type save_mode_: str
        :param renames_: One-on-one mapping with data-frame fields, if they are to be renamed
        :type renames_: List[str]
        :param write_op_: ES writing operation type e.g. upsert
        :type write_op_: str
        :param mapping_id_: Column to be used for document mapping in ES
        :type mapping_id_: str

        :return: Writes data in Spark DataFrame to ES index
        :rtype: None
        """
        if renames_:
            df_ = df_.toDF(*renames_)

        writer_ = self._add_es_attributes(df_.write, self.elastic_ip, self.elastic_port)
        if write_op_:
            writer_ = writer_.option(SparkESConstants.ES_KEY_WRITE_OP, write_op_)
        if mapping_id_:
            writer_ = writer_.option(SparkESConstants.ES_KEY_MAPPING_ID, mapping_id_)
        writer_.mode(save_mode_).save(index_)
