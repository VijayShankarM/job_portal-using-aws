import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobTable')  # Ensure this matches your actual table name

def lambda_handler(event, context):
    try:
        # Fetch all job listings from DynamoDB
        response = table.scan()

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Allow all origins
                'Access-Control-Allow-Methods': 'OPTIONS, GET',  # Allowed HTTP methods
                'Access-Control-Allow-Headers': 'Content-Type'  # Allowed headers
            },
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, GET',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
