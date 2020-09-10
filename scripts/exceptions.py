from scripts.send_email import Email
from scripts.s3_repository import S3Repository
import json


class Exceptions:
    def __init__(self):
        pass

    def send_alert(self, subject, exception_message, link_url=""):
        email = Email(subject, exception_message, link_url)
        email.send_email()

    def save_to_dynamo_error(self, **kwargs):
        subject = 'Write to DynamoDB failed'
        exception_message = kwargs['exception_message']
        link_url = kwargs['link_url']
        self.send_alert(subject, exception_message, link_url)

    def file_validation_failed(self, **kwargs):
        s3_repo = S3Repository()
        body = kwargs['body']
        bucket_name = kwargs['bucket_name']
        key = kwargs['key']
        metadata = 'Validation failed'
        email_subject = 'Validation failed'
        email_body = kwargs['email_body']
        upload_response = s3_repo.save_to_bucket(body=body,
                                                 bucket_name=bucket_name,
                                                 key=key,
                                                 metadata=metadata,
                                                 save_belron_copy=False)
        email_link = upload_response['object_url']
        response_body = "The file validation FAILED. The admin team have been sent an alert"
        self.send_alert(email_subject, email_body, email_link)
        return {
            'statusCode': 400,
            'body': json.dumps(response_body)
        }

    def exception_missing_s3(self, **kwargs):
        s3_repo = S3Repository()
        body = kwargs['body']
        bucket_name = kwargs['bucket_name']
        key = kwargs['key']
        metadata = 'The file could not be allocated to a S3 bucket. Ensure the device number maps to a country code'
        email_subject = 'Non domiciled bucket'
        email_body = kwargs['email_body']
        upload_response = s3_repo.save_to_bucket(body=body,
                                                 bucket_name=bucket_name,
                                                 key=key,
                                                 metadata=metadata,
                                                 save_belron_copy=False)
        email_link = upload_response['object_url']
        response_body = "The file has been received but could not be allocated to a Business Unit. " \
                        "The admin team have been sent an alert"
        self.send_alert(email_subject, email_body, email_link)
        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }

    def no_country_for_old_men(self, **kwargs):
        s3_repo = S3Repository()
        body = kwargs['body']
        bucket_name = kwargs['bucket_name']
        key = kwargs['key']
        metadata = 'The file could not be allocated to a Business Unit due to an unknown device number'
        email_subject = 'Missing S3 bucket'
        email_body = "An attempt to reconcile a file to a device and country code FAILED."
        upload_response = s3_repo.save_to_bucket(body=body,
                                                 bucket_name=bucket_name,
                                                 key=key,
                                                 metadata=metadata,
                                                 save_belron_copy=False)
        email_link = upload_response['object_url']
        response_body = "The file could not be uploaded as the device number is unknown. " \
                        "The admin team have been sent an alert"
        self.send_alert(email_subject, email_body, email_link)
        return {
            'statusCode': 400,
            'body': json.dumps(response_body)
        }

    def write_to_dynamo_exception(self, **kwargs):
        s3_repo = S3Repository()
        body = kwargs['body']
        bucket_name = kwargs['bucket_name']
        key = kwargs['key']
        metadata = 'The file could not be the dynamo db table'
        email_subject = 'File data could not be written to the dynamo db table'
        email_body = kwargs['email_body']
        upload_response = s3_repo.save_to_bucket(body=body,
                                                 bucket_name=bucket_name,
                                                 key=key,
                                                 metadata=metadata,
                                                 save_belron_copy=False)
        email_link = upload_response['object_url']
        response_body = "The file could not be uploaded as the write process was interrupted. " \
                        "The admin team have been sent an alert"
        self.send_alert(email_subject, email_body, email_link)
        return {
            'statusCode': 400,
            'body': json.dumps(response_body)
        }

    def file_upload_error(self, **kwargs):
        s3_repo = S3Repository()
        body = kwargs['body']
        bucket_name = kwargs['bucket_name']
        key = kwargs['key']
        metadata = 'The file presented with a problem when uploading to S3'
        email_subject = 'Invalid xml'
        email_body = kwargs['email_body']
        upload_response = s3_repo.save_to_bucket(body=body,
                                                 bucket_name=bucket_name,
                                                 key=key,
                                                 metadata=metadata,
                                                 save_belron_copy=False)
        email_link = upload_response['object_url']
        response_body = "The file could not be uploaded. This may be because the file already exists in the S3 bucket. " \
                        "The admin team have been sent an alert"
        self.send_alert(email_subject, email_body, email_link)
        return {
            'statusCode': 400,
            'body': json.dumps(response_body)
        }

    def exception_handler(self, **kwargs):
        s3_repo = S3Repository()
        error_object = kwargs['error_object']
        body = kwargs['body']
        bucket_name = kwargs['bucket_name']
        key = kwargs['key']
        metadata = 'Failed validation on {0}'.format(error_object.__class__.__name__)

        upload_response = s3_repo.save_to_bucket(body=body,
                                                 bucket_name=bucket_name,
                                                 key=key, metadata=metadata,
                                                 save_belron_copy=False)
        email_link = upload_response['object_url']
        if error_object.__class__.__name__ == 'ExpatError':
            email_subject = 'Invalid xml'
            email_body = "A submitted file FAILED one or more checks for valid xml. " \
                         "The error is reported as: {0}:".format(error_object)
            response_body = "Validation FAILED for this file due to an incomplete or missing tag. " \
                            "The admin team have been sent an alert"
        elif error_object.__class__.__name__ == 'IndexError':
            email_subject = 'Missing tag'
            email_body = "A submitted file FAILED one or more checks for valid xml. " \
                         "The error is reported as: {0}:".format(error_object)
            response_body = "Validation for this file FAILED due to an Index Error. " \
                            "The admin team have been sent an alert"
        else:
            email_subject = 'Error on validation'
            email_body = "A submitted file FAILED one or more checks for valid xml. " \
                         "The error is reported as: {0}:".format(error_object)
            response_body = "Validation for this file FAILED. The admin team have been sent an alert"

        self.send_alert(email_subject, email_body, email_link)

        return {
            'statusCode': 400,
            'body': json.dumps(response_body)
        }
