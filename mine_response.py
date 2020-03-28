import json
import os
import time
from urllib.request import Request, urlopen

SECONDS_DELAY = 10


def mine_response(request):
    data = request.get_json()
    if data["token"] != os.getenv("SLACK_TOKEN"):
        return "Forbidden", 200

    response_url = data["response_url"]
    text = data["text"]
    message = {
        "response_type": "in_channel",
        "text": f"Completed: {text}",
    }

    # Execute some tasks...
    time.sleep(SECONDS_DELAY)

    # Send Slack Message
    req = Request(
        response_url,
        data=json.dumps(message).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urlopen(req) as res:
        print(res.read().decode())

    return "ok"
