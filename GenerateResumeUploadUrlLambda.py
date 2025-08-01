import json
import boto3
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = 'course-docs-bucket'  # 🪣 Update to your actual S3 bucket name

def lambda_handler(event, context):
    document_id = str(uuid.uuid4())
    key = f"enrollments/{document_id}.pdf"  # 📂 Changed from 'resumes/' to 'enrollments/'

    upload_url = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key, 'ContentType': 'application/pdf'},
        ExpiresIn=3600
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps({'uploadUrl': upload_url, 'fileName': key})
    }
