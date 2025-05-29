from constructs import Construct
from aws_cdk import Stack
from nba_dfs_demo_cdk.constructs.storage import RawEmailFilesBucket, CsvStorageBucket
from nba_dfs_demo_cdk.constructs.email import EmailService
from nba_dfs_demo_cdk.constructs.processing import CsvProcessor

class NbaDfsDemoCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create S3 storage
        self.raw_email_storage = RawEmailFilesBucket(self, "RawEmailStorage")
        self.storage = CsvStorageBucket(self, "CsvStorage")

        # Create SES service
        self.email_service= EmailService(
            self,
            "EmailService",
            storage_bucket=self.storage.bucket
        )

        # Create Lambda and connect to the S3 bucket
        self.processor = CsvProcessor(
            self, 
            "CsvProcessor",
            storage_bucket=self.storage.bucket
        )
