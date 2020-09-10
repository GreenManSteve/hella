import xlrd
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from scripts.send_email import Email
dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table('Hella-Gutmann')


class Device:
    def __init__(self, device_number):
        self.device_number = device_number
        self.__product = None
        self.__customer_name = None
        self.__country_code = None

    def get_device_number(self):
        return self.device_number

    # internal private methods
    def __set_product(self, val):
        self.__product = val

    def __get_product(self):
        return self.__product

    def __set_customer_name(self, val):
        self.__customer_name = val

    def __get_customer_name(self):
        return self.__customer_name

    def __set_country_code(self, val):
        self.__country_code = val

    def get_country_code(self):
        return self.__country_code

    def load_by_device_number(self, device_no_value):
        try:
            response = table.query(
                # Add the name of the index you want to use in your query.
                IndexName="PK-SK-index",
                KeyConditionExpression=Key('PK').eq('device_no-{}'.format(device_no_value)) & Key('SK').eq('device_no-{}'.format(device_no_value)),
            )
            count = response['Count']
            if count > 0:
                self.__set_country_code(response['Items'][0]['country_code'])
                self.__set_customer_name(response['Items'][0]['customer_name'])
                self.__set_product(response['Items'][0]['product'])
                return True
            else:
                return False
        except ClientError:
            email = Email(subject="Client Error", body_text="A Client Error occurred when attempting to reference "
                                                            "index <i>PK-SK-index</i>. Check that the index exists "
                                                            "on table Hella-Gutmann")
            email.send_email()
            return False
