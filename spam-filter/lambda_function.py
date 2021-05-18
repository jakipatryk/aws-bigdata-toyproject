import json
import boto3
import os
import base64

sagemaker = boto3.client("runtime.sagemaker")
endpoint_name = os.environ["SAGEMAKER_ENDPOINT_NAME"]
lambda_client = boto3.client("lambda")
ip_filter_lambda_arn = os.environ["IP_FILTER_ARN"]

def extract_review_full_text(base64_data):
    data = json.loads(base64.b64decode(base64_data))
    return data["review_title"] + " " + data["review_text"]

def get_predictions(reviews):
    response = sagemaker.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=json.dumps(reviews)
    )
    return json.loads(response["Body"].read().decode())

def filter_ips(event):
    ip_filter_response = lambda_client.invoke(
        FunctionName=ip_filter_lambda_arn,
        InvocationType="RequestResponse",
        Payload=json.dumps(event)
    )
    return json.load(ip_filter_response["Payload"])

def lambda_handler(event, context):
    event = filter_ips(event)
    records = event["records"]
    filtering_result = {
        r["recordId"]: r["result"] \
            if (extract_review_full_text(r["data"]) != " ") else "Dropped"
        for r in records
    }
    reviewsWithId = [
        (r["recordId"], extract_review_full_text(r["data"]))
        for r in records if filtering_result[r["recordId"]] != "Dropped"
    ]
    predictions = get_predictions(list(map(lambda r: r[1], reviewsWithId)))
    for r, p in zip(reviewsWithId, predictions):
        if p == 1:
            filtering_result[r[0]] = "Dropped"
    return {
        "records": [
            {
                "recordId": record["recordId"],
                "result": filtering_result[record["recordId"]],
                "data": record["data"]
            } for record in records
        ]
    }