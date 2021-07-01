import argparse
import glob
import os
from csv import reader
from dataclasses import asdict, dataclass
from pathlib import Path

import boto3
import tqdm

NUM_OF_ITEMS_BEFORE_ITEM_DISPLAY = 9


@dataclass
class FashionItem:
    id: int
    gender: str
    masterCategory: str
    subCategory: str
    articleType: str
    baseColor: str
    season: str
    year: int
    usage: str
    productDisplayName: str
    imagePath: str = "nan"

    def add_url(self):
        self.imagePath = (
            f"https://statis-s3-bucket.s3.eu-west-1.amazonaws.com/images/{self.id}.jpg"
        )

    def convert_to_db_type(self):
        for attr in list(vars(self).keys()):
            val = vars(self)[attr]
            if self.__annotations__[attr] == str:
                setattr(self, attr, {"S": val})
            else:
                # dynamodb can't handle empty numbers
                if not val:
                    setattr(self, attr, {"S": val})
                else:
                    setattr(self, attr, {"N": val})


def load_data(args):
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url="http://localhost:4566",
        use_ssl=False,
        region_name="eu-west-1",
    )

    images_in_dataset = [
        int(Path(img).stem) for img in glob.glob(args.path_to_images + "*.jpg")
    ]

    with open(args.csv_file) as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header is not None:
            for row in tqdm.tqdm(csv_reader):
                item = FashionItem(
                    *row[:NUM_OF_ITEMS_BEFORE_ITEM_DISPLAY],
                    productDisplayName=",".join(row[NUM_OF_ITEMS_BEFORE_ITEM_DISPLAY:]),
                )
                if int(item.id) in images_in_dataset:
                    item.add_url()

                item.convert_to_db_type()

                dynamodb.put_item(TableName="FashionProducts", Item=asdict(item))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--meta",
        action="store",
        required=True,
        dest="csv_file",
        help="metadata for dataset",
    )

    parser.add_argument(
        "--images",
        action="store",
        required=True,
        dest="path_to_images",
        help="path to folder of images",
    )

    args = parser.parse_args()

    load_data(args)
