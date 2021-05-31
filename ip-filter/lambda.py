import json
import base64
import boto3
import os

dynamodb_client = boto3.client(
    "dynamodb", region_name=os.environ["DYNAMO_REGION"])


def extract_user_ip(base64_data):
    return json.loads(base64.b64decode(base64_data))["user_ip"]


def get_suspicious_ips(ips, batch_size=90):
    table = os.environ["TABLE_NAME"]
    suspicious_ips = set()
    for i in range(0, len(ips), batch_size):
        batch = ips[i:(i + batch_size)]
        response = dynamodb_client.batch_get_item(
            RequestItems={
                f"{table}": {
                    "Keys": [{"user_ip": {"S": user_ip}} for user_ip in ips]
                }
            }
        )
        suspicious_ips |= {r["user_ip"]["S"]
                           for r in response["Responses"][f"{table}"]}
    return suspicious_ips


def lambda_handler(event, context):
    ips = list({extract_user_ip(record["data"])
                for record in event["records"]})
    suspicious_ips = get_suspicious_ips(ips)
    return {
        "records": [
            {
                "recordId": record["recordId"],
                "result": "Dropped" if (extract_user_ip(record["data"]) in suspicious_ips) else "Ok",
                "data": record["data"]
            } for record in event["records"]
        ]
    }
