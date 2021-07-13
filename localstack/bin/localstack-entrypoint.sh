#!/bin/bash

readonly LOCALSTACK_URL=http://localhost:4566

aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
echo "[default]" > ~/.aws/config
echo "region = us-east-1" >> ~/.aws/config
echo "output = json" >> ~/.aws/config


printf "Configuring localstack components..."

# create and upload to S3
# awslocal s3 mb "s3://static-s3-bucket"

# # lambda + sqs
# awslocal lambda create-function --function-name s3-copy-lambda --code ImageUri=s3-copy-lambda:latest --role arn:aws:iam::000000000:role/lambda-ex

# awslocal sqs create-queue --queue-name s3-queue

# # bound to lambdas
# awslocal lambda create-event-source-mapping \
#  --function-name s3-copy-lambda --batch-size 1 \
#  --event-source-arn arn:aws:sqs:us-east-1:000000000000:s3-queue
