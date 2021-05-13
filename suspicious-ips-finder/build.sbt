name := "suspicious-ips-finder"

version := "0.1"

scalaVersion := "2.11.12"

libraryDependencies += "com.typesafe" % "config" % "1.4.1"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.3.3"
libraryDependencies += "com.audienceproject" %% "spark-dynamodb" % "0.4.4"
libraryDependencies += "org.apache.spark" %% "spark-yarn" % "2.3.0" % "provided"
libraryDependencies += "org.scalactic" %% "scalactic" % "3.2.2"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.2" % "test"
