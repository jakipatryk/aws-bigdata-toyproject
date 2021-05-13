import com.typesafe.config.{Config, ConfigFactory}
import org.apache.spark.sql.SparkSession

object Driver extends App with SuspiciousIpsFinder with DataLoader with DataSaver {
  implicit val config: Config = ConfigFactory.load().getConfig(args(0))

  implicit val spark: SparkSession = SparkSession
    .builder()
    .appName("suspicious-ips-finder")
    .master(config.getString("execution.mode"))
    .getOrCreate()

  saveIps(enrichWithExpirationTime(getSuspiciousIps(loadViews())))
}
