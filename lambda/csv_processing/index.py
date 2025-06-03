import json
import boto3
import os

s3 = boto3.client('s3')
ses = boto3.client('ses')

def lambda_handler(event, context):
    # Get the bucket name and file key from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    print(f"Processing file: {file_key} from bucket: {bucket_name}")
    
    # For now, just log that we received the file
    # TODO: Add SES email sending logic here
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully processed {file_key}')
    }