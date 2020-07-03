from behave import *
import os
import logging
import boto3
import uuid
from reflex_acceptance_common import ReflexAcceptance

S3_CLIENT = boto3.client("ec2")
SQS_CLIENT = boto3.client("sqs")
acceptance_client = ReflexAcceptance("s3-bucket-policy-public-access")


def create_bucket():
    """Handles s3-bucket-not-encrypted, s3-logging-not-enabled, s3-bucket-policy-public-access."""
    bucket_name = f"reflex-acceptance-{uuid.uuid4()}"
    create_response = S3_CLIENT.create_bucket(Bucket=bucket_name)
    logging.info("Created instance with response: %s", create_response)
    return bucket_name


def put_public_bucket_policy(bucket_name):
    put_bucket_response = S3_CLIENT.put_bucket_policy(
        Bucket=bucket_name,
        Policy='{"Version": "2012-10-17", "Statement": [{ "Sid": "id-1","Effect": "Allow","Principal": "*" , "Action": [ "s3:GetObject"], "Resource": ["arn:aws:s3:::acl3/*" ] } ]}',
    )
    logging.info("Modified bucket to be public with: %s", put_bucket_response)


def delete_bucket(bucket_name):
    delete_response = S3_CLIENT.delete_bucket(Bucket=bucket_name)
    logging.info("Deleted bucket with: %s", delete_response)


def get_message_from_queue(queue_url):
    message = SQS_CLIENT.receive_message(QueueUrl=queue_url, WaitTimeSeconds=20)
    message_body = message["Messages"][0]["Body"]
    return message_body


@given("the reflex s3-bucket-policy-public-access rule is deployed into an AWS account")
def step_impl(context):
    assert acceptance_client.get_queue_url_count("S3BucketPolicyPublicAccess-DLQ") == 1
    assert acceptance_client.get_queue_url_count("S3BucketPolicyPublicAccess") == 2
    assert acceptance_client.get_queue_url_count("test-queue") == 1
    sqs_test_response = SQS_CLIENT.list_queues(QueueNamePrefix="test-queue")
    context.config.userdata["test_queue_url"] = sqs_test_response["QueueUrls"][0]


@given("an s3 bucket is created and available")
def step_impl(context):
    bucket_name = create_bucket()
    context.config.userdata["bucket_name"] = bucket_name


@when("a bucket policy with public access is associated with the bucket")
def step_impl(context):
    put_public_bucket_policy(context.config.userdata.get("bucket_name"))


@then("a reflex alert message is sent to our reflex SNS topic")
def step_impl(context):
    message = get_message_from_queue(context.config.userdata["test_queue_url"])
    print(message)
    assert "Public Access" in message
    assert "Reflex" in message
    delete_bucket(context.config.userdata["bucket_name"])
