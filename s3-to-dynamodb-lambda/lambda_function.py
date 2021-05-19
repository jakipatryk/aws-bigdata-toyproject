import json
import boto3
import os
import csv
import codecs

s3 = boto3.resource("s3")
dynamodb = boto3.resource("dynamodb")

table_name = os.environ["DYNAMODB_TABLE_NAME"]

def write_to_dynamodb(batch):
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch_writer:
        for item in batch:
            batch_writer.put_item(Item=item)

def lambda_handler(event, context):
    objs = []
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        file_name = record["s3"]["object"]["key"]
        objs.append(s3.Object(bucket, file_name).get()["Body"])
    batch_size = 100
    batch = []
    for obj in objs:
        for row in csv.DictReader(codecs.getreader("utf-8")(obj)):
            batch.append(row)
            if len(batch) >= batch_size:
                write_to_dynamodb(batch)
                batch.clear()
    if batch:
        write_to_dynamodb(batch)
    return {
        'statusCode': 200,
        'body': json.dumps('Uploaded to DynamoDB Table')
    }

