import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

S3_BUCKET = 'job-res-port'
TABLE_NAME = 'ApplicantTable'

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }

    try:
        body = json.loads(event['body'])

        name = body['name']
        dob = body['dob']
        email = body['email']
        phone = body['phone']
        jobname = body['jobname']
        companyname = body['companyname']
        address = body['address']
        resume_data = body['resume']

        if not resume_data.startswith('JVBERi0'):
            raise Exception("Uploaded file is not a valid PDF format")

        file_name = f"{uuid.uuid4()}.pdf"
        file_content = base64.b64decode(resume_data)

        s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=file_content, ContentType='application/pdf')

        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'applicantId': str(uuid.uuid4()),
            'name': name,
            'dob': dob,
            'email': email,
            'phone': phone,
            'jobname': jobname,
            'companyname': companyname,
            'address': address,
            'resumeKey': file_name
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Application submitted successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
