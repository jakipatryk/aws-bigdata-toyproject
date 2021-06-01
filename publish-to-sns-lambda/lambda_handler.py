import json
import boto3
import os
import base64

sns_arn = os.environ["SNS_ARN"]

sns = boto3.client("sns")


def lambda_handler(event, context):
    views_count = json.loads(
        base64.b64decode(event["records"][0]["data"]))["TOP_10_VIEWS_COUNT"]
    sns.publish(
        TargetArn=sns_arn,
        Message=json.dumps(
            {"default": f"Too many views for top 10 items: {views_count}"}),
        MessageStructure='json'
    )
    return {
        "records": [
            {"recordId": r["recordId"], "result": "Ok"} for r in event["records"]
        ]
    }
