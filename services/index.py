import json
import boto3
import os
import uuid

# Environment and DynamoDB setup
table_name = os.environ.get("TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

# Helper functions
def generate_response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*"
        }
    }

def add_new_item(item_data):
    item_data["id"] = str(uuid.uuid4())
    table.put_item(Item=item_data)
    return generate_response(200, {"id": item_data["id"]})

def get_item_by_id(item_id):
    response = table.get_item(Key={"id": item_id})
    if "Item" in response:
        return generate_response(200, response["Item"])
    return generate_response(404, "Not found")

# Lambda handler function
def handler(event, context):
    method = event.get("httpMethod")

    if method == "POST":
        item_data = json.loads(event["body"])
        return add_new_item(item_data)

    if method == "GET":
        item_id = event.get("queryStringParameters", {}).get("id")
        if item_id:
            return get_item_by_id(item_id)
        return generate_response(400, "Missing item ID in query parameters")

    return generate_response(405, "Method not allowed")
