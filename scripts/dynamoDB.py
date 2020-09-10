import datetime
from scripts.hash import sha_3_hex_digest
from scripts.html import clean_html
from scripts.base import Base
from scripts.deleteItem import DeleteItem
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError, ParamValidationError, MissingParametersError
from scripts.exceptions import Exceptions
import boto3
client = boto3.client('dynamodb')
dynamo_db = boto3.resource('dynamodb')


class DynamoDB(Base):
    def __init__(self, records_to_write, table_name):
        Base.__init__(self)
        self.__table = table_name
        self.__records_list = records_to_write

    def get_table(self):
        return self.__table

    def __get_records_list(self):
        return self.__records_list

    def save_to_dynamo_db(self):
        function_completed = False
        status_code = 400
        status_message = "No Records saved"
        try:
            put_list = list()
            i_count = 0

            count_down = len(self.__get_records_list())
            for write_element in self.__get_records_list():
                item = dict()
                for element in write_element:
                    item.update({element: write_element[element]})
                i_count += 1
                count_down -= 1
                put_element = {'Item': item}
                put_list.append({'PutRequest': put_element})
                if i_count <= 25 and count_down > 0:
                    if self.__batch_save(put_list):
                        put_list.clear()
                        i_count = 0
                        function_completed = True
                        status_code = 200
                        status_message = "Records saved"
                    else:
                        function_completed = False
                elif i_count <= 25 and count_down == 0:
                    if self.__batch_save(put_list):
                        put_list.clear()
                        i_count = 0
                        function_completed = True
                        status_code = 200
                        status_message = "Records saved"
                    else:
                        print("raise err")
                        function_completed = False
                        status_code = 400
                        status_message = "An error in logic occurred when attempted to save the xml data"
                else:
                    function_completed = False
                    status_code = 400
                    status_message = "A record or set of records was not caught in the batching logic"

        except (ClientError, ParamValidationError, MissingParametersError) as error:
            function_completed = False
            status_code = 400
            status_message = "An error of type {0} occurred when trying to write " \
                            "records to the DynamoDB table".format(error)

        except SyntaxError as error:
            function_completed = False
            status_code = 400
            status_message = "A syntax error of type {0} occurred when trying to write " \
                            "records to the DynamoDB table".format(error)

        response = {'function_completed': function_completed,
                    'statusCode': status_code,
                    'statusMessage': status_message}
        return response

    def __batch_save(self, my_list):
        response = client.batch_write_item(
            RequestItems={
                'Hella-Gutmann':
                    my_list
            },
            ReturnConsumedCapacity='INDEXES',
            ReturnItemCollectionMetrics='SIZE'
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False

