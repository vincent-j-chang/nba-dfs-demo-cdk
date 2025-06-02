# FILE: nba_dfs_demo_cdk/constructs/email_extraction.py
from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_iam as iam,
    Duration,
)
from constructs import Construct


class EmailExtraction(Construct):
    def __init__(self, scope: Construct, id: str, raw_email_bucket: s3.Bucket, csv_bucket: s3.Bucket, **kwargs):
        super().__init__(scope, id)
        
        # Store the bucket reference
        self.storage_bucket = csv_bucket
        self.raw_email_storage = raw_email_bucket 
        
        # Create Lambda function
        self.lambda_function = _lambda.Function(
            self,
            "EmailExtractionFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("lambda/email_extraction/"),
            timeout=Duration.minutes(5),  # Email processing might take some time
            memory_size=512,  # Enough memory for Email processing
            environment={
                "SOURCE_BUCKET": raw_email_bucket.bucket_name,
                "DESTINATION_BUCKET": csv_bucket.bucket_name
            }
        )
        
        # Grant Lambda permission to read from raw email bucket and write to CSV bucket
        raw_email_bucket.grant_read(self.lambda_function)
        csv_bucket.grant_write(self.lambda_function)
        
        # Set up S3 event notification to trigger Lambda
        raw_email_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(self.lambda_function)
        )