""" Module for S3BucketPolicyPublicAccess """

import json
import os

import boto3
from reflex_core import AWSRule


class S3BucketPolicyPublicAccess(AWSRule):
    """ Detect when a bucket has a Bucket Policy that grant public access. """

    def __init__(self, event):
        super().__init__(event)

    def extract_event_data(self, event):
        """ Extract required event data """
        self.bucket_name = event["detail"]["requestParameters"]["bucketName"]

    def resource_compliant(self):
        """
        Determine if the resource is compliant with your rule.

        Return True if it is compliant, and False if it is not.
        """

        for statement in self.event["detail"]['requestParameters'][
                "bucketPolicy"]["Statement"]:
            if statement["Principal"] == "*":
                return False
        return True

    def get_remediation_message(self):
        """ Returns a message about the remediation action that occurred """
        return f"The S3 bucket {self.bucket_name} contains a Bucket Policy " \
               f"that grants Public Access. "


def lambda_handler(event, _):
    """ Handles the incoming event """
    rule = S3BucketPolicyPublicAccess(json.loads(event["Records"][0]["body"]))
    rule.run_compliance_rule()
