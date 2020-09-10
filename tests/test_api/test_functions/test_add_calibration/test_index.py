import os
import unittest
from unittest import mock

from api.functions.hella.add_calibration.index import handler


class TestIndex(unittest.TestCase):

    @mock.patch("aws_xray_sdk.core.xray_recorder.begin_subsegment")
    @mock.patch("aws_xray_sdk.core.xray_recorder.end_subsegment")
    def test_handler_text_xml(self, end_sub_seg_mock, beging_sub_seg_mock):
        end_sub_seg_mock.return_value = None
        beging_sub_seg_mock.return_value = None

        os.environ['LAMBDA_TASK_ROOT'] = 'LAMBDA_TASK_ROOT' # Must be present for functions using x-ray tracing

        headers = {"headers": {"Content-Type": "text/xml"}}
        body = {"body": ""}
        event = {}
        event.update(**headers, **body)
        resp = handler(event, None)

        expected = {
                    "statusCode": 200,
                    "body": "ok",
                    "headers": {"Content-Type": "application/json"},
                }
        self.assertDictEqual(expected, resp)

    @mock.patch("aws_xray_sdk.core.xray_recorder.begin_subsegment")
    @mock.patch("aws_xray_sdk.core.xray_recorder.end_subsegment")
    def test_handler_app_xml(self, end_sub_seg_mock, beging_sub_seg_mock):
        end_sub_seg_mock.return_value = None
        beging_sub_seg_mock.return_value = None

        os.environ['LAMBDA_TASK_ROOT'] = 'LAMBDA_TASK_ROOT' # Must be present for functions using x-ray tracing

        headers = {"headers": {"Content-Type": "application/xml"}}
        body = {"body": ""}
        event = {}
        event.update(**headers, **body)
        resp = handler(event, None)

        expected = {
                    "statusCode": 200,
                    "body": "ok",
                    "headers": {"Content-Type": "application/json"},
                }
        self.assertDictEqual(expected, resp)

    @mock.patch("aws_xray_sdk.core.xray_recorder.begin_subsegment")
    @mock.patch("aws_xray_sdk.core.xray_recorder.end_subsegment")
    def test_handler_invalid_content_type(self, end_sub_seg_mock, beging_sub_seg_mock):
        end_sub_seg_mock.return_value = None
        beging_sub_seg_mock.return_value = None

        os.environ['LAMBDA_TASK_ROOT'] = 'LAMBDA_TASK_ROOT' # Must be present for functions using x-ray tracing

        headers = {"headers": {"Content-Type": "text/html"}}
        body = {"body": ""}
        event = {}
        event.update(**headers, **body)
        resp = handler(event, None)

        expected = {
                    "statusCode": 400,
                    "body": "Invalid Content Type Provided",
                    "headers": {"Content-Type": "application/json"},
                }
        self.assertDictEqual(expected, resp)

    @mock.patch("aws_xray_sdk.core.xray_recorder.begin_subsegment")
    @mock.patch("aws_xray_sdk.core.xray_recorder.end_subsegment")
    def test_handler_invalid_request_type(self, end_sub_seg_mock, beging_sub_seg_mock):
        end_sub_seg_mock.return_value = None
        beging_sub_seg_mock.return_value = None

        os.environ['LAMBDA_TASK_ROOT'] = 'LAMBDA_TASK_ROOT' # Must be present for functions using x-ray tracing

        headers = {}
        body = {"body": ""}
        event = {}
        event.update(**headers, **body)
        resp = handler(event, None)

        expected = {
                    "statusCode": 400,
                    "body": "Invalid Request Type",
                    "headers": {"Content-Type": "application/json"},
                }
        self.assertDictEqual(expected, resp)
