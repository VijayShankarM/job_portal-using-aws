import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

S3_BUCKET = 'course-resumes'  # 🪣 Replace with your actual S3 bucket name
TABLE_NAME = 'StudentApplications'  # 🪧 Replace with your actual DynamoDB table name

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Methods': '*'
    }

    try:
        body = json.loads(event['body'])

        studentName = body['studentName']
        birthDate = body['birthDate']
        email = body['email']
        phone = body['phone']
        courseName = body['courseName']
        instituteName = body['instituteName']
        address = body['address']
        resume_data = body['resume']

        if not resume_data.startswith('JVBERi0'):
            raise Exception("Uploaded file is not a valid PDF format")

        file_name = f"{uuid.uuid4()}.pdf"
        file_content = base64.b64decode(resume_data)

        s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=file_content, ContentType='application/pdf')

        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'applicationId': str(uuid.uuid4()),
            'studentName': studentName,
            'birthDate': birthDate,
            'email': email,
            'phone': phone,
            'courseName': courseName,
            'instituteName': instituteName,
            'address': address,
            'resumeKey': file_name
        })

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Enrollment submitted successfully'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
