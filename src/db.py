import boto3


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
        pass
