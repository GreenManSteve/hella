import logging
import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# patch(["boto3"])  # can patch botocore, boto3, requests, sqlite3, mysql (use patch_all() to patch all at once)


# WANT TO TRY THIS: https://docs.aws.amazon.com/lambda/latest/dg/python-tracing.html


def handler(event, context):
    logger.info("## EVENT: add_calibration : STARTED")

    logger.info("## ENVIRONMENT VARIABLES")
    logger.info(os.environ)
    try:
        xray_recorder.begin_subsegment('add_calibration')
        if "headers" in event:
            headers = event["headers"]
            logger.info("## HEADERS")
            logger.info(headers)

            if "Content-Type" in headers:
                content_type = headers["Content-Type"]

                if content_type == "text/xml":
                    # do text/xml things

                    parse_xml(event["body"])

                    # CURRENT IMPLEMENTATION
                    # PARSE XML
                    # GET ID
                    # GET DATE
                    # WRITE TO S3 using ID AND DATE (think we may change this?)
                    # Respond "OK"... << we will do this for legacy but seems pretty non descript

                    print(str(event["body"]))
                    return {
                        "statusCode": 200,
                        "body": 'ok',
                        "headers": {"Content-Type": "application/json"},
                    }

                elif content_type == "application/xml":  # Not sure if we need to do anything different here - but here for now
                    # do application/xml things
                    parse_application_xml(event["body"])
                    print(str(event["body"]))
                    return {
                        "statusCode": 200,
                        "body": 'ok',
                        "headers": {"Content-Type": "application/json"},
                    }
                else:
                    print(str(event["body"]))
                    # Throw an error of some sort
                    return {
                        "statusCode": 400,
                        "body": "Invalid Content Type Provided",
                        "headers": {"Content-Type": "application/json"},
                    }

        return {
            "statusCode": 400,
            "body": "Invalid Request Type",
            "headers": {"Content-Type": "application/json"},
        }
    finally:
        xray_recorder.end_subsegment()


@xray_recorder.capture('parse_xml')
def parse_xml(text):
    return 0


@xray_recorder.capture('parse_application_xml')
def parse_application_xml(text):
    return 0
