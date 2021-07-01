import functools
import operator

import boto3
from boto3.dynamodb.conditions import Key


class DB:
    """
    class for working with DynamoDB
    """

    TABLE_NAME = "FashionProducts"

    def __init__(self, endpoint_url="http://localhost:4566"):
        dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint_url,
            use_ssl=False,
            region_name="eu-west-1",
        )

        self._table = dynamodb.Table(self.TABLE_NAME)

    def query_key_dict(self, keys: dict):
        fe = self._reduce_by_and_list_of_keys(keys)
        return self._scan(fe)

    def _reduce_by_and_list_of_keys(self, keys: dict):
        fe_list = list()
        for k, v in keys.items():
            key = getattr(Key(k), v[0])(v[1])
            fe_list.append(key)

        return functools.reduce(operator.and_, fe_list)

    def _scan(self, fe: Key):

        response = self._table.scan(FilterExpression=fe)

        items = response["Items"]

        while "LastEvaluatedKey" in response:
            response = self._table.scan(
                FilterExpression=fe, ExclusiveStartKey=response["LastEvaluatedKey"]
            )

            items.extend(response["Items"])

        return items
