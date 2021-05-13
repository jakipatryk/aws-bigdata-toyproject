import com.typesafe.config.Config
import org.apache.spark.sql.types.{StringType, StructType, TimestampType}
import org.apache.spark.sql.{DataFrame, SparkSession}

import java.util.Calendar

trait DataLoader {
  /***
   * Loads all views logs from the current day.
   */
  def loadViews()(implicit spark: SparkSession, config: Config): DataFrame = {
    val schema = new StructType()
      .add("item_id", StringType)
      .add("user_ip", StringType)
      .add("device_type", StringType)
      .add("device_id", StringType)
      .add("timestamp", TimestampType)

    val now = Calendar.getInstance()
    val datePathSuffix = s"/${now.get(Calendar.YEAR)}" +
      s"/${calendarIntFormatter(now.get(Calendar.MONTH) + 1)}" +
      s"/${calendarIntFormatter(now.get(Calendar.DAY_OF_MONTH))}" +
      s"/*"

    spark
      .read
      .schema(schema)
      .json(config.getString("input.base.dir") + datePathSuffix)
  }

  private def calendarIntFormatter(i: Int): String = {
    if (i >= 10) i.toString else s"0$i"
  }
}
