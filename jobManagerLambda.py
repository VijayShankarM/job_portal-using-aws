import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CourseTable')  # 🗂 Renamed from JobTable

def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        body = json.loads(event['body'])

        if method == 'PUT':
            if isinstance(body, list):
                body = body[0]  # Handle array input like [ {...} ]

            course_id = body.get('courseId')
            title = body.get('title')
            description = body.get('description')
            instructor = body.get('instructor')
            deadline = body.get('deadline')

            if not course_id:
                return respond(400, {'error': 'Missing courseId for update'})

            # Update item in DynamoDB
            response = table.update_item(
                Key={'courseId': course_id},
                UpdateExpression="SET title = :t, description = :d, instructor = :i, deadline = :dl",
                ExpressionAttributeValues={
                    ':t': title,
                    ':d': description,
                    ':i': instructor,
                    ':dl': deadline
                },
                ReturnValues="UPDATED_NEW"
            )

            return respond(200, {'message': 'Course updated', 'updatedAttributes': response.get('Attributes')})

        elif method == 'DELETE':
            course_id = body.get('courseId')
            if not course_id:
                return respond(400, {'error': 'Missing courseId for deletion'})

            table.delete_item(Key={'courseId': course_id})
            return respond(200, {'message': 'Course deleted'})

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
