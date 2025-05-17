# FILE: nba_dfs_demo_cdk/constructs/storage.py
from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class CsvStorageBucket(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id)

        # Create S3 bucket to store CSV files
        self.bucket = s3.Bucket(
            self, 
            "CsvBucket",
            removal_policy=RemovalPolicy.RETAIN,  # Protect against accidental deletion
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable encryption
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Security best practice
        )
        
        # Add lifecycle rule to move older files to cheaper storage
        self.bucket.add_lifecycle_rule(
            id="ArchiveRule",
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=Duration.days(30)
                )
            ],
            expiration=Duration.days(90)  # Delete files after 90 days
        )