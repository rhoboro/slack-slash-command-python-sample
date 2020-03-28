import json
import os

from google.cloud import tasks_v2

client = tasks_v2.CloudTasksClient()


def mine(request):
    if "token" not in request.form or request.form["token"] != os.getenv("SLACK_TOKEN"):
        return "Forbidden", 403

    parent = client.queue_path(os.getenv("PROJECT"), os.getenv("LOCATION"), os.getenv("QUEUE_NAME"))
    task = {
        "http_request": {
            "http_method": "POST",
            "url": os.getenv("QUEUE_URL"),
            "body": json.dumps(request.form.to_dict(flat=True)).encode(),
            "headers": {"Content-Type": "application/json"},
        }
    }
    client.create_task(parent, task)

    text = request.form["text"]
    response = {
        "response_type": "in_channel",
        "text": f"Started: {text}",
    }
    return json.dumps(response), 200, {"Content-Type": "application/json"}
