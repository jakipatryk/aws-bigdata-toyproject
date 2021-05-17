import argparse
import os
import sys
import csv
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from sagemaker_containers.beta.framework import encoders

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--train', type=str, default=os.environ['SM_CHANNEL_TRAIN'])

    args = parser.parse_args()
    
    csv.field_size_limit(sys.maxsize)

    f = os.path.join(args.train, "spam_or_not_spam.csv")
    dataset = pd.read_csv(f, engine="python").dropna()

    vectorizer = CountVectorizer().fit(dataset["email"])

    X = vectorizer.transform(dataset["email"])
    y = dataset["label"]

    clf = LogisticRegression().fit(X, y)

    joblib.dump(vectorizer, os.path.join(args.model_dir, "vectorizer.joblib"))
    joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))

def input_fn(input_data, content_type):
    return [s.lower() for s in encoders.decode(input_data, content_type)]

def model_fn(model_dir):
    vectorizer = joblib.load(os.path.join(model_dir, "vectorizer.joblib"))
    clf = joblib.load(os.path.join(model_dir, "model.joblib"))
    return vectorizer, clf

def predict_fn(input_object, model):
    vectorizer, clf = model
    return clf.predict(vectorizer.transform(input_object))