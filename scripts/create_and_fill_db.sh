# #!/bin/bash

# create DB table
awslocal dynamodb create-table --cli-input-json file://scripts/table-definition.json

# fill DB
python scripts/data/load_metadata.py --meta ../dataset/styles.csv --images ../dataset/images/

# create and upload to S3
awslocal s3 mb "s3://static-s3-bucket"

awslocal s3 \
  sync ../dataset/images/ \
 "s3://static-s3-bucket/images/"
