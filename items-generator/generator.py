import csv
import json
import random
import boto3
import os

FILE_NAME = "items_description.csv"

with open("../config.json") as f:
    config = json.load(f)

def create_item(item_id):
    title = f"item #{item_id}"
    description = f"description of item #{item_id}"
    category = str(random.randint(1, config["num_of_categories"]))
    return str(item_id), title, description, category

items = [create_item(item_id) for item_id in range(config["num_of_items"])]

with open(FILE_NAME, "w") as f:
    csv_writer = csv.writer(f)
    header = ("item_id", "title", "description", "category")
    csv_writer.writerow(header)
    for item in items:
        csv_writer.writerow(item)

s3_client = boto3.client("s3")
try:
    s3_client.upload_file(FILE_NAME, config["bucket"], f"static/{FILE_NAME}")
finally:
    os.remove(FILE_NAME)
