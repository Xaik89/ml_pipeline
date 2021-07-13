import json
import logging
import os

import boto3

S3_NAME = "static-s3-bucket"
s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566",
    use_ssl=False,
    region_name="us-east-1",
)


def handler(event, context):
    message = json.loads(event)
    body_dict = json.loads(message["Records"][0]["body"])
    items = body_dict["items"]
    name_folder = body_dict["name_folder_in_s3"]

    for img in items:
        s3_client.copy_object(
            Bucket=S3_NAME,
            CopySource=os.path.join(S3_NAME, "images", img),
            Key=os.path.join(name_folder, img),
        )

    return {"statusCode": 200, "body": json.dumps("List of files copied")}
