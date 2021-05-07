import json
import base64
import boto3
import os

dynamodb_client = boto3.client("dynamodb", region_name=os.environ["DYNAMO_REGION"])

def extract_user_ip(base64_data):
    return json.loads(base64.b64decode(base64_data))["user_ip"]

def is_suspicious(user_ip):
    response = dynamodb_client.get_item(
        TableName=os.environ["TABLE_NAME"],
        Key={"user_ip": {"S": user_ip}}
    )
    return "Item" in response

def lambda_handler(event, context):
    return {
        "records": [
            {
                "recordId": record["recordId"],
                "result": "Dropped" if is_suspicious(extract_user_ip(record["data"])) else "Ok",
                "data": record["data"]
            } for record in event["records"]
        ]
    }
