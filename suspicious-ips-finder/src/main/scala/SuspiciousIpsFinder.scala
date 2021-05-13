import org.apache.spark.sql.functions.{count, from_unixtime, lit, max, min, unix_timestamp}
import org.apache.spark.sql.types.LongType
import org.apache.spark.sql.{DataFrame, SparkSession}

trait SuspiciousIpsFinder {

  def getSuspiciousIps(views: DataFrame)(implicit spark: SparkSession): DataFrame = {
    import spark.implicits._

    views
      .groupBy($"user_ip")
      .agg(
        count(lit(1)) as "views_count",
        min($"timestamp").cast(LongType) as "min_timestamp",
        max($"timestamp").cast(LongType) as "max_timestamp"
      )
      .where(
        ($"views_count" / ($"max_timestamp" - $"min_timestamp" + lit(1))) >= lit(5)
      )
      .select($"user_ip")
  }

  /***
   * Adds column `expires_on` with epoch timestamp of 24h from now.
   */
  def enrichWithExpirationTime(suspiciousIps: DataFrame)(implicit spark: SparkSession): DataFrame = {
    suspiciousIps
      .withColumn("expires_on", unix_timestamp() + lit(24 * 60 * 60))
  }

}
