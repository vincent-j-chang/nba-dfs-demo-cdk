import os
import boto3
import email
from email import policy
from email.parser import BytesParser

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the source S3 bucket name and file key from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Get the destination S3 bucket name from environment variable
    destination_bucket = os.environ['CSV_BUCKET_NAME']

    # Download the email object from the S3 bucket
    email_object = s3.get_object(Bucket=source_bucket, Key=file_key)
    
    # Parse the email object
    msg = BytesParser(policy=policy.default).parsebytes(email_object['Body'].read())
    
    # Check if the email object has any attachments
    for part in msg.walk():
        # Check if part is an attachment
        if part.get_content_disposition() == 'attachment':
            file_name = part.get_filename()
            if file_name.endswith('.csv'):  # Check if the attachment is a CSV
                try:
                    # Save the attachment to the destination bucket with the original filename
                    s3.put_object(
                        Bucket=destination_bucket,
                        Key=file_name,
                        Body=part.get_payload(decode=True)
                    )
                    
                    print(f"CSV attachment '{file_name}' copied to '{destination_bucket}' successfully.")
                except Exception as e:
                    print(f"Error saving CSV attachment '{file_name}' to '{destination_bucket}': {str(e)}")
                    raise e

    return {
        'statusCode': 200,
        'body': 'CSV attachments processed successfully'
    }