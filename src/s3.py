import json
import os
from io import BytesIO

import boto3
from PIL import Image

from utils import DecimalEncoder


class S3:
    """
    class for s3
    """

    S3_NAME = "static-s3-bucket"

    def __init__(self, endpoint_url="http://localhost:4566"):
        self._endpoint_url = endpoint_url
        self._s3_client = boto3.client(
            "s3", endpoint_url=endpoint_url, use_ssl=False, region_name="us-east-1"
        )

        self._s3_res = boto3.resource(
            "s3", endpoint_url=endpoint_url, use_ssl=False, region_name="us-east-1"
        )

    def copy_file_in_bucket(self, source: str, dest: str):
        self._s3_client.copy_object(
            Bucket=self.S3_NAME, CopySource=os.path.join(self.S3_NAME, source), Key=dest
        )

    def save_metadata(self, dest: str, metadata: dict):
        self._s3_client.put_object(
            Bucket=self.S3_NAME,
            Body=(bytes(json.dumps(metadata, cls=DecimalEncoder).encode("UTF-8"))),
            Key=dest,
        )

    def gen_of_images(self, folder: str):
        paginator = self._s3_client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(Bucket=self.S3_NAME, Prefix=folder)

        for page in page_iterator:
            if page["KeyCount"] > 0:
                for item in page["Contents"]:
                    if "jpg" not in item["Key"]:
                        continue

                    file_byte_string = self._s3_client.get_object(
                        Bucket=self.S3_NAME, Key=item["Key"]
                    )["Body"].read()

                    yield Image.open(BytesIO(file_byte_string)), item["Key"]

    def save_new_image(self, image, name: str):
        buffer = BytesIO()
        image.save(buffer, format="jpeg")
        buffer.seek(0)
        self._s3_client.put_object(Bucket=self.S3_NAME, Key=name, Body=buffer)

    def load_meta_data(self, file_name):
        obj = self._s3_res.Object(self.S3_NAME, file_name)
        meta_json = obj.get()["Body"].read().decode("utf-8")
        return json.loads(meta_json)

    def get_n_random_images(self, path_to_folder, num_of_images):
        images = []
        for i, (img, path) in enumerate(self.gen_of_images(path_to_folder)):
            if i >= num_of_images:
                break
            images.append(
                (
                    img,
                    os.path.join(
                        "https://statis-s3-bucket.s3.us-east-1.amazonaws.com/images",
                        path.split("/")[-1],
                    ),
                )
            )
        return images
