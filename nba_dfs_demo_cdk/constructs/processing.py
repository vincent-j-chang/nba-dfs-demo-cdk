# FILE: nba_dfs_demo_cdk/constructs/processing.py
from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
    aws_iam as iam,
    Duration,
)
from constructs import Construct


class CsvProcessor(Construct):
    def __init__(self, scope: Construct, id: str, storage_bucket: s3.Bucket, **kwargs):
        super().__init__(scope, id)
        
        # Store the bucket reference
        self.storage_bucket = storage_bucket
        
        # Create Lambda function
        self.lambda_function = _lambda.Function(
            self,
            "CsvProcessorFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("lambda/process_csv"),
            timeout=Duration.minutes(5),  # CSV processing might take some time
            memory_size=512,  # Enough memory for CSV processing
            environment={
                "BUCKET_NAME": storage_bucket.bucket_name
            }
        )
        
        # Grant Lambda permission to read from S3 bucket
        storage_bucket.grant_read(self.lambda_function)
        
        # Set up S3 event notification to trigger Lambda
        storage_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(self.lambda_function),
            s3.NotificationKeyFilter(suffix=".csv")  # Only trigger for CSV files
        )