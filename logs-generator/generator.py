import json
import random
import time
import os
import shutil
import subprocess
import sys
import boto3
from kiner.producer import KinesisProducer
from datetime import datetime

VIEWS_SLEEP_SECONDS = 0.1
REVIEWS_SLEEP_SECONDS = 1

with open("../config.json") as f:
    config = json.load(f)

def create_fake_view():
    item_id = random.randint(1, config["num_of_items"])
    user_ip = f"{random.randint(11, 191)}.{random.randint(1, 223)}." \
              f"{random.randint(1, 254)}.{random.randint(1, 254)}"
    device_type = random.choice(config["device_types"])
    device_id = random.randint(1, config["num_of_devices"])
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
            "item_id": str(item_id),
            "user_ip": user_ip,
            "device_type": device_type,
            "device_id": str(device_id),
            "timestamp": timestamp
           }

def get_reviews():
    path = "real_reviews.tsv"
    if not os.path.exists(path):
        subprocess.check_call([
            "curl",
            "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip",
            "-o",
            "/tmp/smsspamcollection.zip",
        ])

        subprocess.check_call([
            "unzip", "-o", "/tmp/smsspamcollection.zip", "-d", "/tmp/dataset"
        ])

        shutil.move("/tmp/dataset/SMSSpamCollection", path)
        os.remove("/tmp/smsspamcollection.zip")
        shutil.rmtree("/tmp/dataset", ignore_errors=True)

    with open(path) as f:
        lines = [line.split("\t", 1)[-1].lower() for line in f.read().splitlines()]

    return lines

REVIEWS = get_reviews()

def create_fake_review():
    item_id = random.randint(1, config["num_of_items"])
    user_ip = f"{random.randint(11, 191)}.{random.randint(1, 223)}." \
              f"{random.randint(1, 254)}.{random.randint(1, 254)}"
    device_type = random.choice(config["device_types"])
    device_id = random.randint(1, config["num_of_devices"])
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    review = random.choice(REVIEWS)
    review_title = " ".join(review.split()[:3])
    review_text = " ".join(review.split()[3:])
    review_stars = random.randint(0, 5)
    return {
            "item_id": str(item_id),
            "user_ip": user_ip,
            "device_type": device_type,
            "device_id": str(device_id),
            "timestamp": timestamp,
            "review_title": review_title,
            "review_text": review_text,
            "review_stars": review_stars
           }   


def logs_generator(create_single_log_function, sleep_duration):
    while True:
        log = create_single_log_function()
        yield json.dumps(log)
        time.sleep(sleep_duration)
       
def stream_to_kinesis(stream, logs):
    producer = KinesisProducer(
        stream_name=stream,
        batch_size=100,
        batch_time=1,
        max_retries=10,
        kinesis_client=boto3.client("kinesis", region_name=config["region"]))
    
    try:
        for record in logs:
            print(record)
            producer.put_record(record + "\n")
    finally:
        producer.close()

what_to_stream = sys.argv[1].lower()
if what_to_stream == "views":
    stream_to_kinesis(
        config["views_stream_name"],
        logs_generator(create_fake_view, VIEWS_SLEEP_SECONDS))
elif what_to_stream == "reviews":
    stream_to_kinesis(
        config["reviews_stream_name"],
        logs_generator(create_fake_review, REVIEWS_SLEEP_SECONDS))
else:
    raise ValueError("Bad CLI argument, should be either 'views' or 'reviews'.")
