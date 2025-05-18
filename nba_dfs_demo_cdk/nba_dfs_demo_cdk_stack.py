# FILE: nba_dfs_demo_cdk/nba_dfs_demo_cdk_stack.py
from aws_cdk import (
    Stack,
    # Add any additional imports here
)
from constructs import Construct
from nba_dfs_demo_cdk.constructs.storage import CsvStorageBucket


class NbaDfsDemoCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create the S3 bucket for CSV storage
        self.storage = CsvStorageBucket(self, "CsvStorage")
        
        # We'll add SES and Lambda components later