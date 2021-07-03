#!/bin/bash

# create s3 bucket
aws s3 mb --endpoint-url="http://localhost:4566" --region eu-west-1 "s3://static-s3-bucket"

# create DB table
aws --endpoint-url="http://localhost:4566" dynamodb create-table --cli-input-json file://scripts/data/table-definition.json

# fill DB
python scripts/data/load_metadata.py --meta dataset/styles.csv --images dataset/images/

# upload to S3
aws s3 --endpoint-url="http://localhost:4566" \
 --region eu-west-1 sync dataset/images/* \
 "s3://static-s3-bucket/images/"
