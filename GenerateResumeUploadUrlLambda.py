import json
import boto3
import uuid

s3 = boto3.client('s3')
BUCKET_NAME = 'job-res-port'

def lambda_handler(event, context):
    resume_id = str(uuid.uuid4())
    key = f"resumes/{resume_id}.pdf"
    
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
