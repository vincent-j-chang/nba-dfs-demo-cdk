from constructs import Construct
from aws_cdk import Stack
from nba_dfs_demo_cdk.constructs.storage import RawEmailFilesBucket, CsvStorageBucket
from nba_dfs_demo_cdk.constructs.email import EmailService
from nba_dfs_demo_cdk.constructs.processing import CsvProcessor
from nba_dfs_demo_cdk.constructs.email_extraction import EmailExtraction

class NbaDfsDemoCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create S3 storage
        self.raw_email_storage = RawEmailFilesBucket(self, "RawEmailStorage")
        self.csv_bucket = CsvStorageBucket(self, "CsvStorage")

        # Create SES service
        self.email_service= EmailService(
            self,
            "EmailService",
            storage_bucket=self.raw_email_storage.bucket
        )

        # Lambda to Extract Email
        self.email_extractor = EmailExtraction(
            self,
            "EmailExtraction",
            raw_email_bucket = self.raw_email_storage.bucket,
            csv_bucket = self.csv_bucket.bucket
        )

        # Lambda to Process CSVs
        self.processor = CsvProcessor(
            self, 
            "CsvProcessor",
            storage_bucket=self.csv_bucket.bucket
        )
