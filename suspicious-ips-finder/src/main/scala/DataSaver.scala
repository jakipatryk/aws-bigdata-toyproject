import com.typesafe.config.Config
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}
import com.audienceproject.spark.dynamodb.implicits._

trait DataSaver {

  def saveIps(ips: DataFrame)(implicit spark: SparkSession, config: Config): Unit = {
    val outputMode = config.getString("output.mode")
    if(outputMode == "file") {
      ips
        .write
        .mode(SaveMode.Append)
        .json(config.getString("output.base.dir"))
    } else if(outputMode == "dynamodb") {
      ips
        .write
        .option("region", config.getString("output.dynamodb.region"))
        .dynamodb(config.getString("output.dynamodb.table"))
    }
  }

}
