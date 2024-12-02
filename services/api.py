import json

from flask import Flask, request

from services.db import (
    add_new_item, get_all_items, get_item_by_id, delete_item_by_id
)

app = Flask(__name__)


@app.route("/api/todos", methods=["POST"])
def handle_post():
    item_data = json.loads(request.data)
    return add_new_item(item_data)


@app.route("/api/todos", methods=["GET"])
def handle_get_all():
    return get_all_items()


@app.route("/api/todos/<todo_id>", methods=["GET"])
def handle_get(todo_id):
    item = get_item_by_id(todo_id)
    return item if item else {"description": "Not found"}, 404



@app.route("/api/todos/<todo_id>", methods=["DELETE"])
def handle_delete(todo_id):
    delete_item_by_id(todo_id)
    return '', 204
