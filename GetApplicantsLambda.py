import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ApplicantTable')

s3 = boto3.client('s3')
BUCKET_NAME = 'job-res-port'

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])

        for item in items:
            resume_key = item.get('resumeKey')
            if resume_key:
                item['resumeUrl'] = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': resume_key},
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
