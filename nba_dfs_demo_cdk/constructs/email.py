# FILE: nba_dfs_demo_cdk/constructs/email.py
from aws_cdk import (
    aws_ses as ses,
    aws_ses_actions as actions,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct


class EmailService(Construct):
    def __init__(self, scope: Construct, id: str, storage_bucket: s3.Bucket, **kwargs):
        super().__init__(scope, id)
        
        # Store the bucket reference
        self.storage_bucket = storage_bucket
        
        # Create SES Receipt Rule Set with rules
        self.rule_set = ses.ReceiptRuleSet(
            self,
            "CsvEmailRuleSet",
            rules=[
                ses.ReceiptRuleOptions(
                    recipients=["dfs-demo-org.awsapps.com"],  # Replace with your domain
                    actions=[
                        actions.S3(
                            bucket=storage_bucket,
                            object_key_prefix="incoming-emails/"
                        )
                    ]
                )
            ]
        )