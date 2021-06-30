#!/bin/bash

# create DB table
aws --endpoint-url="http://localhost:4566" dynamodb create-table --cli-input-json file://scripts/data/table-definition.json

# fill DB
python load_metadata.py --meta dataset/style.csv --images dataset/images/

# upload to S3
aws s3 --endpoint-url="http://localhost:4566" \
 --region eu-west-1 cp dataset/images/* \
 "s3://statis-s3-bucket/images/"