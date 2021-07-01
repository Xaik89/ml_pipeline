# built-in
import json
import os
import typing as t

# third party
import albumentations as A
import boto3
import numpy as np
from PIL import Image

from db import DB

# local
from s3 import S3


class API_AWS:
    """
    simple api for AWS services
    """

    def __init__(self):
        self._db = DB()
        self._s3 = S3()

    def query_male_shoes_from_2012(self):
        query_dict = {
            "gender": ["eq", "Men"],
            "subCategory": ["eq", "Shoes"],
            "year": ["gt", 2012],
        }
        name_folder_in_s3 = "query_male_shoes_from_2012"

        self._general_query(query_dict, name_folder_in_s3, True)

    def query_woman_footwear_sports_2011(self):
        query_dict = {
            "gender": ["eq", "Woman"],
            "masterCategory": ["eq", "Footwear"],
            "usage": ["eq", "Sports"],
            "year": ["eq", 2011],
        }
        name_folder_in_s3 = "query_woman_footwear_sports_2011"

        self._general_query(query_dict, name_folder_in_s3)

    def query_unisex_heels_casual_2011(self):
        query_dict = {
            "gender": ["eq", "Unisex"],
            "subCategory": ["eq", "Heels"],
            "usage": ["eq", "Casual"],
            "year": ["eq", 2011],
        }
        name_folder_in_s3 = "query_unisex_heels_casual_2011"

        self._general_query(query_dict, name_folder_in_s3)

    def query_male_shoes_from_2012_albu(self):
        query_dict = {
            "gender": ["eq", "Men"],
            "subCategory": ["eq", "Shoes"],
            "year": ["gt", 2012],
        }
        name_folder_in_s3 = "query_male_shoes_from_2012_with_albu"

        self._general_query(query_dict, name_folder_in_s3, True)

    def query_male_shoes_from_2012_pytorch(self):
        query_dict = {
            "gender": ["eq", "Men"],
            "subCategory": ["eq", "Shoes"],
            "year": ["gt", 2012],
        }
        name_folder_in_s3 = "query_male_shoes_from_2012_with_cv"

        self._general_query(
            query_dict, name_folder_in_s3, run_albumentations=False, run_cv_model=True
        )

    def _general_query(
        self,
        query_dict,
        name_folder_in_s3,
        run_albumentations=False,
        run_cv_model=False,
    ):

        # first step: query to DB
        items = self._db.query_key_dict(query_dict)[:10]

        # second step: save output to S3
        self._save_to_s3_all_data(items, name_folder_in_s3)

        # for step 3,4: I assume, that requirements were to work on results on s3
        # if not, I wouldn't save images in step 2

        # third step: run albumentation if needed
        if run_albumentations:
            self._run_albumentations(name_folder_in_s3)

        # fourth step: run CV model
        if run_cv_model:
            self._run_cv_model(name_folder_in_s3)

    def _save_to_s3_all_data(self, items, name_folder_in_s3):
        pass

    def _run_albumentations(self, folder_with_images):
        pass

    def _run_cv_model(self):
        pass


if __name__ == "__main__":
    api = API_AWS()

    api.query_male_shoes_from_2012()
