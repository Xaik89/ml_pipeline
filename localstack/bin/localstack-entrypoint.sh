#!/bin/bash

readonly LOCALSTACK_URL=http://localhost:4566

aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
echo "[default]" > ~/.aws/config
echo "region = us-east-1" >> ~/.aws/config
echo "output = json" >> ~/.aws/config
