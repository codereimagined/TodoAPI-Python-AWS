import json
import boto3
import os
import uuid

from flask import Flask, request

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


app = Flask(__name__)

@app.route("/api", methods=["POST"])
def handle_post():
    item_data = json.loads(request.data)
    return add_new_item(item_data)


@app.route("/api", methods=["GET"])
def handle_get():
    item_id = request.args.get("id")
    if item_id:
        return get_item_by_id(item_id)
    return generate_response(400, "Missing item ID in query parameters")
