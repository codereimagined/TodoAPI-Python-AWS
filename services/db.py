import boto3
import os
import uuid

# Environment and DynamoDB setup
table_name = os.environ.get("TABLE_NAME")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)


# Helper functions
def add_new_item(item_data):
    item_data["id"] = str(uuid.uuid4())
    table.put_item(Item=item_data)
    return {"id": item_data["id"]}


def get_item_by_id(item_id):
    response = table.get_item(Key={"id": item_id})
    if "Item" in response:
        return response["Item"]
    return {"description": "Not found"}, 404


def delete_item_by_id(item_id):
    table.delete_item(Key={"id": item_id})


def get_all_items():
    response = table.scan()
    return response["Items"]
