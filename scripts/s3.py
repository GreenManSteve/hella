import boto3
import botocore.exceptions
from scripts.country import Country
client = boto3.client('s3')


class S3:
    def __init__(self):
        self.__bucket_name = None
        self.__region = None
        self.__access = None

    def get_bucket_name(self):
        return self.__bucket_name

    def __set_bucket_name(self, val):
        self.__bucket_name = val

    def get_region(self):
        return self.__region

    def __set_region(self, val):
        self.__region = val

    def get_access(self):
        return self.__access

    def __set_access(self, val):
        self.__access = val

    def get_date_created(self):
        return self.__date_created

    def __set_date_created(self, val):
        self.__date_created = val

    def load_by_country_code(self, country_code):
        """
            :param country_code: ISO Alpha-2.e.g United Kingdom GB, France FR
            :return: boolean value to denote load operation success | failure
            """
        __loaded_successfully = False
        self.__bucket_name = self.__build_bucket(country_code)
        s3_temp = self.__build_bucket(country_code)
        s3_exists = self.check_bucket_exists(s3_temp)
        if s3_exists:
            __bucket_location = self.get_bucket_location(s3_temp)
            __bucket_access = self.get_bucket_access_policy(s3_temp)
            if __bucket_location and __bucket_access:
                __loaded_successfully = True
                return __loaded_successfully
            else:
                return __loaded_successfully
        else:
            return __loaded_successfully

    def __build_bucket(self, country_code):
        bucket_name = "{0}-hella-calibrations".format(self.__get_country_by_code(country_code))
        return bucket_name.lower()

    def __get_country_by_code(self, country_code):
        country = Country(country_code)
        belron_country_code = country.get_belron_country_code()
        if belron_country_code is None:
            return "none"
        else:
            return belron_country_code

    def check_bucket_exists(self, s3_temp):
        try:
            response = client.head_bucket(
                Bucket=s3_temp
            )
            if response is not None:
                return True
            else:
                return False
        except botocore.exceptions.ClientError:
            return False

    def get_bucket_location(self, s3_temp):
        try:
            response = client.get_bucket_location(
                Bucket=s3_temp
            )
            if response is not None:
                self.__set_region(response['LocationConstraint'])
                return True
            else:
                return False
        except botocore.exceptions.ClientError as error:
            print("write to log S3.py line 74")
            return False

    def get_bucket_access_policy(self, s3_temp):
        try:
            response = client.get_bucket_acl(
                Bucket=s3_temp
            )
            if response is not None:
                self.__set_access(response['Grants'][0]['Permission'])
                return True
            else:
                self.__set_access('none')
                return False
        except botocore.exceptions.ClientError as error:
            print("write to log S3.py line 74")
            return False