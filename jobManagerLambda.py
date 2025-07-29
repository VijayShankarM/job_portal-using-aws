import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('JobTable')  # Replace with your actual table name

def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        body = json.loads(event['body'])
        
        if method == 'PUT':
            if isinstance(body, list):
                body = body[0]  # Handle array input like [ {...} ]
            
            job_id = body.get('jobId')
            title = body.get('title')
            description = body.get('description')
            company = body.get('company')
            deadline = body.get('deadline')

            if not job_id:
                return respond(400, {'error': 'Missing jobId for update'})

            # Update item in DynamoDB
            response = table.update_item(
                Key={'jobId': job_id},
                UpdateExpression="SET title = :t, description = :d, company = :c, deadline = :dl",
                ExpressionAttributeValues={
                    ':t': title,
                    ':d': description,
                    ':c': company,
                    ':dl': deadline
                },
                ReturnValues="UPDATED_NEW"
            )

            return respond(200, {'message': 'Job updated', 'updatedAttributes': response.get('Attributes')})

        elif method == 'DELETE':
            job_id = body.get('jobId')
            if not job_id:
                return respond(400, {'error': 'Missing jobId for deletion'})

            table.delete_item(Key={'jobId': job_id})
            return respond(200, {'message': 'Job deleted'})

        else:
            return respond(405, {'error': 'Method not allowed'})

    except Exception as e:
        return respond(500, {'error': f"Internal server error: {str(e)}"})

def respond(status, body):
    return {
        'statusCode': status,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(body)
    }
