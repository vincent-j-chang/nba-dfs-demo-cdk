import json
import boto3
import os
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib.parse

# Initialize the S3 and SES clients
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

def lambda_handler(event, context):
    # Extract the S3 bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Decode the file key to handle spaces encoded as '+'
    decoded_file_key = urllib.parse.unquote_plus(file_key)

    print(f"Bucket: {bucket_name}")
    print(f"Decoded File Key: {decoded_file_key}")

    # Download the CSV file from S3
    file_name = decoded_file_key.split('/')[-1]
    local_file_path = f'/tmp/{file_name}'
    
    print(f"Attempting to download {file_name} to {local_file_path}")

    try:
        s3_client.download_file(bucket_name, decoded_file_key, local_file_path)
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error downloading file: {e.response["Error"]["Message"]}')
        }

    # Define email parameters
    sender_email = 'vincentchang.dev@gmail.com'  # This needs to be a verified SES email
    receiver_email = 'vincentchang.dev@gmail.com'
    subject = 'Processed CSV File'
    body_text = f'Your CSV file "{file_name}" has been processed successfully. Please find the attached file.'

    # Create a multipart/mixed parent container
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create a multipart/alternative child container
    msg_body = MIMEMultipart('alternative')

    # Encode the text content and set the character encoding
    textpart = MIMEText(body_text.encode('utf-8'), 'plain', 'utf-8')

    # Add the text part to the child container
    msg_body.attach(textpart)

    # Attach the multipart/alternative child container to the multipart/mixed parent container
    msg.attach(msg_body)

    # Define the attachment part and encode it using MIMEApplication
    try:
        with open(local_file_path, 'rb') as f:
            att = MIMEApplication(f.read())
        att.add_header('Content-Disposition', 'attachment', filename=file_name)
        
        # Attach the file to the message
        msg.attach(att)
    except Exception as e:
        print(f"Error reading file for attachment: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error reading file for attachment: {str(e)}')
        }

    # Try to send the email with the attachment
    try:
        response = ses_client.send_raw_email(
            Source=sender_email,
            Destinations=[receiver_email],
            RawMessage={'Data': msg.as_string()}
        )
        print(f'Email sent! Message ID: {response["MessageId"]}')
    except ClientError as e:
        print(f'Error sending email: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email: {e.response["Error"]["Message"]}')
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully processed and emailed {file_name}. Message ID: {response["MessageId"]}')
    }