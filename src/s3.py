import os

import boto3


class S3:
    """
    class for s3
    """

    S3_NAME = "statis-s3-bucket"

    def __init__(self, endpoint_url="http://localhost:4566"):
        self._s3 = boto3.client(
            "s3", endpoint_url=endpoint_url, use_ssl=False, region_name="eu-west-1"
        )

    def copy_file_in_bucket(self, source: str, dest: str):
        pass

    def save_metadata(self, dest: str, metadata: dict):
        pass

    def gen_of_images(self, folder: str):
        pass

    def save_new_image(self, image, name):
        pass
