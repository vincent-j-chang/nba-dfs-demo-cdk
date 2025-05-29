# FILE: nba_dfs_demo_cdk/constructs/storage.py
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
)
from constructs import Construct


class RawEmailFilesBucket(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id)

        # Create S3 bucket to store raw email files from SES
        self.bucket = s3.Bucket(
            self, 
            "RawEmailBucket",
            bucket_name="nba-dfs-demo-cdk-raw-email",
            removal_policy=RemovalPolicy.RETAIN,  # Protect against accidental deletion
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable encryption
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Security best practice
        )


class CsvStorageBucket(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id)

        # Create S3 bucket to store extracted CSV files
        self.bucket = s3.Bucket(
            self, 
            "CsvBucket",
            bucket_name="nba-dfs-demo-cdk-csv",
            removal_policy=RemovalPolicy.RETAIN,  # Protect against accidental deletion
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable encryption
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Security best practice
        )