import boto3
from boto3.dynamodb.types import TypeDeserializer
from uuid import uuid4
import json


def create_item(event, context):
    if 'title' not in event['body'] or 'task' not in event['body']:
        response = {"statusCode": 400, "body": "Please provide title and task"}
    else:
        input_data = json.loads(event['body'])
        title = input_data['title']
        task = input_data['task']
        dynamodb = boto3.client('dynamodb', region_name="us-east-1")
        unique_id = str(uuid4())
        try:
            result = dynamodb.put_item(TableName='Todo',
                                       Item={'UUID': {'S': unique_id}, 'Title': {'S': title}, 'Task': {'S': task}})
            if result['ResponseMetadata']['HTTPStatusCode'] == 200:
                response = {"statusCode": 200,
                            "body": "Your todo item has been inserted successfully! Go " + task + "!"}
            else:
                response = {"statusCode": 400,
                            "body": "There was an error inserting your todo item! Please try again"}

        except Exception as e:
            response = {"statusCode": 400, "body": "There was an error inserting your todo item! Please try again"}

    return response


def fetch_items(event, context):
    unique_id = None
    if 'body' in event and event['body']:
        input_data = json.loads(event['body'])
        unique_id = input_data['id']

    dynamodb = boto3.client('dynamodb', region_name="us-east-1")

    if unique_id:
        response = dynamodb.query(
            TableName='Todo',
            KeyConditionExpression='#id = :uuid',
            ProjectionExpression='Title, Task, #id',
            ExpressionAttributeNames={'#id': 'UUID'},
            ExpressionAttributeValues={':uuid': {'S': unique_id}}
        )
    else:
        response = dynamodb.scan(
            TableName='Todo'
        )

    result = {"statusCode": 200, "body": ""}
    items = []
    for value in response['Items']:
        item = {}
        for key in value:
            item[key] = value[key]["S"]
        items.append(item)
    result["body"] = json.dumps(items)
    return result
