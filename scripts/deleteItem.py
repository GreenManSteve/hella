from scripts.base import Base
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table('Hella-Gutmann')


class DeleteItem(Base):
    def __init__(self, device_no, file_id):
        self.device_no = device_no
        self.file_id = file_id
        self.__delete_items()

    def __delete_items(self):
        items = self.__get_items()
        for i in items:
            table.delete_item(
                Key={
                    'PK': i['PK'],
                    'SK': i['SK']
                }
            )

    def __get_items(self):
        pk = self.device_no
        sk = self.file_id

        response = table.query(
            KeyConditionExpression=Key('PK').eq(pk) & Key('SK').begins_with(sk)
        )
        return response['Items']


