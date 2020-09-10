import json
from datetime import datetime
from xml.dom.minidom import parseString
from xml.parsers.expat import ParserCreate, ExpatError, errors
from scripts.s3_repository import S3Repository
from scripts.xml_input import XmlInput
from scripts.dynamoDB import DynamoDB
from scripts.s3 import S3
from scripts.exceptions import Exceptions
from scripts.xml_hella_gutmann import Xml_Hella_gutmann



def handler(event, context):
    """
    :param event: AWS event
    :param context: context in which the event occurred
    :return: Response that can be interrogated by API gateway
    """
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y %H:%M:%S")
    body = event['data']
    try:
        doc = parseString(body)
        s3_repo = S3Repository()
        xml_file = XmlInput(doc)
        xml_file.validate_fields()
        key = "{0}-{1}.xml".format(xml_file.get_device_no(), xml_file.get_id())
        body = event['data']
        if xml_file.get_validation_pass():
            s3 = S3()
            country_code = xml_file.get_country_code()
            if s3.load_by_country_code(country_code=country_code):
                bucket_name = s3.get_bucket_name()
                metadata = "Re-calibration for {0} submitted {1}".format(country_code.upper(), datetime.today())
                response = s3_repo.save_to_bucket(body, bucket_name, key, metadata)
                if response['saved_result']:
                    bucket_name = response['bucket_name']
                    file_id = response['file_id']
                    s3_link = {'bucket_name': bucket_name, 'file_id': file_id}
                    xml_hella_gutmann = Xml_Hella_gutmann(doc, s3_link, country_code)
                    print("get_ok_to_go {}".format(xml_hella_gutmann.get_ok_to_go()))
                    if xml_hella_gutmann.get_ok_to_go():
                        records_to_write = xml_hella_gutmann.get_records_list()
                        dynamo_db = DynamoDB(records_to_write, "Hella-Gutmann")
                        dynamo_response = dynamo_db.save_to_dynamo_db()
                        if dynamo_response['function_completed']:
                            return {
                                'statusCode': 200,
                                'body': json.dumps('File submitted successfully')
                            }
                        else:
                            exception = Exceptions()
                            return exception.file_upload_error(body=body,
                                                               bucket_name='hella-gutmann-failed-validation',
                                                               key=key,
                                                               email_body=dynamo_response['statusMessage'])
                    else:
                        s3_repo.delete_file(bucket=bucket_name, key=key)
                        exception = Exceptions()
                        xml_validation_report = xml_hella_gutmann.get_validation_report()
                        for item in xml_validation_report:
                            xml_file.set_validation_report(item)
                        return exception.write_to_dynamo_exception(body=body,
                                                                   bucket_name='hella-gutmann-failed-validation',
                                                                   email_body=xml_file.get_validation_report(),
                                                                   key='{0}_{1}'.format(dt_string, key))
                else:
                    return {
                        'statusCode': 400,
                        'body': json.dumps('File already submitted')
                    }
            else:
                exception = Exceptions()
                return exception.no_country_for_old_men(body=body,
                                                        bucket_name='hella-gutmann-unreconciled-by-country',
                                                        key=key)

        elif xml_file.validation_passed_for_non_domiciled_bucket():
            exception = Exceptions()
            return exception.exception_missing_s3(body=body,
                                                  bucket_name='hella-gutmann-unreconciled-by-country',
                                                  email_body=xml_file.get_validation_report(),
                                                  key=key)
        else:
            exception = Exceptions()
            return exception.file_validation_failed(body=body,
                                                    bucket_name='hella-gutmann-failed-validation',
                                                    email_body=xml_file.get_validation_report(),
                                                    key='{0}_{1}'.format(dt_string, key))

    except (ExpatError, IndexError) as error:
        exception = Exceptions()
        return exception.exception_handler(error_object=error,
                                           body=body,
                                           bucket_name='hella-gutmann-failed-validation',
                                           key='{0}_error.xml'.format(dt_string))







