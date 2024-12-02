import boto3
import os
import uuid

# Environment and DynamoDB setup
table_name = os.environ.get("TABLE_NAME")
dynamodb = boto3.resource('dynamodb')
# In local dev we need to add DYNAMODB_ENDPOINT_URL=http://host.docker.internal:8000
# We also need to make sure local DynamoDB is running and have table created, see README-local.md
dynamodb_endpoint_url = os.environ.get("DYNAMODB_ENDPOINT_URL")
if dynamodb_endpoint_url:
    dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint_url)
table = dynamodb.Table(table_name)


# Helper functions
def add_new_item(item_data, db_table=table):
    item_data["id"] = str(uuid.uuid4())
    db_table.put_item(Item=item_data)
    return {"id": item_data["id"]}


def get_item_by_id(item_id, db_table=table):
    response = db_table.get_item(Key={"id": item_id})
    if "Item" in response:
        return response["Item"]
    return None


def delete_item_by_id(item_id):
    table.delete_item(Key={"id": item_id})


def get_all_items():
    response = table.scan()
    return response["Items"]
