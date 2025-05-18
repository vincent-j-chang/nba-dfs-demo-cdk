from constructs import Construct
from aws_cdk import (Stack,
                     aws_s3 as s3)



class NbaDfsDemoCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # Create S3 storage
        bucket = s3.Bucket(self, "nba-dfs-demo-cdk")
