import org.apache.spark.sql.{Row, SparkSession}
import org.scalatest.flatspec.AnyFlatSpec

class SuspiciousIpsFinderSpec extends AnyFlatSpec with SuspiciousIpsFinder with FakeDataLoader {

  implicit val spark: SparkSession = SparkSession
    .builder()
    .master("local[*]")
    .appName("SuspiciousIpsFinderSpec")
    .getOrCreate()
  spark.sparkContext.setLogLevel("ERROR")

  "getSuspiciousIps" should "find user_ip's that have average views/s >= 5" in {
    val views = loadViews()

    val ips = getSuspiciousIps(views).collect()

    assert(ips.length == 2)
    assert(ips.contains(Row("96.120.47.159")))
    assert(ips.contains(Row("93.120.120.120")))
  }

}
