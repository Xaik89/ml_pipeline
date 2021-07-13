import argparse
import json
import os

import albumentations as A
import boto3
import numpy as np
import pandas as pd
import torch
from PIL import Image

from db import DB
from pytorch_model import FashionNetVgg16NoBn
from s3 import S3


class API_AWS:
    """
    simple api for AWS services
    """

    def __init__(self):
        self._db = DB()
        self._s3 = S3()

        self._sqs_client = boto3.client(
            "sqs",
            endpoint_url="http://localhost:4566",
            use_ssl=False,
            region_name="us-east-1",
        )

    def query_male_shoes_from_2012(self):
        query_dict = {
            "gender": ["eq", "Men"],
            "subCategory": ["eq", "Shoes"],
            "year": ["gt", 2012],
        }
        name_folder_in_s3 = "query_male_shoes_from_2012_as"

        return self._general_query(query_dict, name_folder_in_s3, False, False)

    def query_woman_footwear_sports_2011(self):
        query_dict = {
            "gender": ["eq", "Woman"],
            "masterCategory": ["eq", "Footwear"],
            "usage": ["eq", "Sports"],
            "year": ["eq", 2011],
        }
        name_folder_in_s3 = "query_woman_footwear_sports_2011"

        return self._general_query(query_dict, name_folder_in_s3)

    def query_unisex_heels_casual_2011(self):
        query_dict = {
            "gender": ["eq", "Unisex"],
            "subCategory": ["eq", "Heels"],
            "usage": ["eq", "Casual"],
            "year": ["eq", 2011],
        }
        name_folder_in_s3 = "query_unisex_heels_casual_2011"

        return self._general_query(query_dict, name_folder_in_s3)

    def query_male_shoes_from_2012_albu(self):
        query_dict = {
            "gender": ["eq", "Men"],
            "subCategory": ["eq", "Shoes"],
            "year": ["gt", 2012],
        }
        name_folder_in_s3 = "query_male_shoes_from_2012_with_albu"

        return self._general_query(query_dict, name_folder_in_s3, True)

    def query_male_shoes_from_2012_pytorch(self):
        query_dict = {
            "gender": ["eq", "Men"],
            "subCategory": ["eq", "Shoes"],
            "year": ["gt", 2012],
        }
        name_folder_in_s3 = "query_male_shoes_from_2012_with_cv"

        return self._general_query(
            query_dict, name_folder_in_s3, run_albumentations=False, run_cv_model=True
        )

    def load_meta_data(self, path_to_folder):
        d = self._s3.load_meta_data(os.path.join(path_to_folder, "metadata.json"))
        return pd.DataFrame(d)

    def get_n_random_images(self, path_to_folder, num_of_images):
        return self._s3.get_n_random_images(path_to_folder, num_of_images)

    def _general_query(
        self,
        query_dict,
        name_folder_in_s3,
        run_albumentations=False,
        run_cv_model=False,
    ):

        # first step: query to DB
        items = self._db.query_key_dict(query_dict)

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

        return name_folder_in_s3

    def _save_to_s3_all_data(self, items, name_folder_in_s3, use_sqs=False):

        if use_sqs:
            # msg -> sqs -> lambda -> s3
            img_pathes = " ".join([str(item["id"]) + ".jpg" for item in items])
            message = {"items": img_pathes, "name_folder_in_s3": name_folder_in_s3}

            self._sqs_client.send_message(
                QueueUrl="http://localhost:4566/000000000000/s3-queue",
                MessageBody=json.dumps(message),
            )
        else:
            # NAIVE approach
            for item in items:
                image_name = str(item["id"]) + ".jpg"
                self._s3.copy_file_in_bucket(
                    os.path.join("images", image_name),
                    os.path.join(name_folder_in_s3, image_name),
                )

        metadata_path = os.path.join(name_folder_in_s3, "metadata.json")
        self._s3.save_metadata(metadata_path, items)

    def _run_albumentations(self, folder_with_images):
        transform = A.Compose(
            [
                A.RandomCrop(width=50, height=70),
                A.Resize(width=256, height=256),
            ]
        )

        for im, path_im in self._s3.gen_of_images(folder_with_images):
            im = np.array(im)
            new_image = transform(image=im)["image"]

            pil_image = Image.fromarray(np.uint8(new_image)).convert("RGB")
            self._s3.save_new_image(pil_image, path_im)

    def _run_cv_model(self, folder_with_images):
        """
        run pytorch model on image from output query
        TODO: complete implementation
        """
        fn = FashionNetVgg16NoBn()

        for im, path_im in self._s3.gen_of_images(folder_with_images):
            im = np.array(im)
            massive_attr, categories = fn(torch.from_numpy(im))

            # next step to update meta file and save it in s3


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        action="store",
        default=1,
        dest="query",
        type=int,
        help="which query to run from 1 up to 5th",
    )

    args = parser.parse_args()
    api = API_AWS()

    if args.query == 1:
        api.query_male_shoes_from_2012()
    elif args.query == 2:
        api.query_woman_footwear_sports_2011()
    elif args.query == 3:
        api.query_unisex_heels_casual_2011()
    elif args.query == 4:
        api.query_male_shoes_from_2012_albu()
    elif args.query == 5:
        api.query_male_shoes_from_2012_pytorch()
