import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EnrollmentTable')  # 🗂 Renamed from ApplicantTable

s3 = boto3.client('s3')
BUCKET_NAME = 'course-docs-bucket'  # 🪣 Renamed from job-res-port

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        for item in items:
            document_key = item.get('documentKey')  # 🧾 Renamed from resumeKey
            if document_key:
                item['documentUrl'] = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': document_key},
                    ExpiresIn=300  # 5 minutes
                )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({'error': str(e)})
        }
