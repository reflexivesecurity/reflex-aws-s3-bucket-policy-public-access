
Feature: This behavior tests the detective mechanism for when a bucket policy in S3 contains public access
  Scenario: A bucket is created with a public policy associated with it.
    Given the reflex s3-bucket-policy-public-access rule is deployed into an AWS account
    And an s3 bucket is created and available
    When a bucket policy with public access is associated with the bucket
    Then a reflex alert message is sent to our reflex SNS topic
