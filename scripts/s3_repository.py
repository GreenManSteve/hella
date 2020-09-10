from scripts.hella_functions import hash_file
from datetime import datetime
import boto3
client = boto3.client('s3')


now = datetime.now()
dt_string = now.strftime("%d%m%Y %H:%M:%S")


class S3Repository:
    def __init__(self):
        pass

    def __put_object(self, body, bucket_name, key, metadata, acl='bucket-owner-full-control'):
        s3 = boto3.resource('s3')
        s3.meta.client.put_object(
            ACL=acl,
            Body=body,
            Bucket=bucket_name,
            Key=key,
            Metadata={
                'string': metadata
            })

    def save_to_bucket(self, body, bucket_name, key, metadata, save_belron_copy=True):
        """
        :param body: xml data sent by client
        :param bucket_name: S3 bucket location. Determined by the device number
        :param key: file name made up of device_no and file id
        :param metadata: country and date of the calibration
        :param save_belron_copy: optional parameter. Where TRUE is upplied a copy ofthe uploaded xml is
        saved to S3 hella-gutmann-belron-copy
        :return: JSON object
        """
        __save = False
        __response_message = None
        __hashed_body = hash_file(body)
        if not self.__file_exists(bucket_name, key):
            self.__put_object(__hashed_body, bucket_name, key, metadata)
            object_url = self.retrieve_public_url(bucket_name, key)
            __save = True
            __response_message = "{0} added to {1}.".format(key, bucket_name)
            if save_belron_copy:
                self.__put_object(body, "hella-gutmann-belron-copy", key, metadata)
        else:
            __response_message = "File {0} already exists in S3 {1}.".format(key, bucket_name)
            __save = False
            object_url = None

        response = {
            'saved_result': __save,
            'bucket_name': bucket_name,
            'file_id': key,
            'response_message': __response_message,
            'object_url': object_url
        }
        return response

    def __file_exists(self, bucket_name, file_id):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        key = file_id
        objs = list(bucket.objects.filter(Prefix=key))
        if len(objs) > 0 and objs[0].key == key:
            return True
        else:
            return False

    def retrieve_public_url(self, s3_bucket_name, s3_file_name):
        """
        Given a s3 bucket name and key this method will figure out the location of the bucket
        and the respective url
        :param s3_bucket_name: S3 bucket name
        :param s3_file_name: S3 file name
        :return: formatted object URL giving publicly accessible URL for object (presuming permissions are set
        accordingly)
        """
        bucket_location = boto3.client('s3').get_bucket_location(Bucket=s3_bucket_name)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'],
            s3_bucket_name,
            s3_file_name)
        return object_url

    def delete_file(self, bucket, key):
        response = client.delete_object(
            Bucket=bucket,
            Key=key
        )
        return response
