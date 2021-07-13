# #!/bin/bash

awslocal lambda create-function --function-name s3-copy-lambda --code ImageUri=s3-copy-lambda:latest --role arn:aws:iam::000000000:role/lambda-ex --timeout 30

awslocal sqs create-queue --queue-name s3-queue

# bound to lambdas
awslocal lambda create-event-source-mapping \
 --function-name s3-copy-lambda --batch-size 1 \
  --event-source-arn arn:aws:sqs:us-east-1:000000000000:s3-queue
