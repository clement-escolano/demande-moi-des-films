import json
import requests


def generate_messaging_events(payload):
    """Generate tuples of (sender_id, message_text) from the
    provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]


def send_message(token, recipient, text, options=None):
    """Send the message text to recipient with id recipient.
    """
    if options is not None:
        buttons = []
        for option in options:
            buttons.append({
                "type":    "postback",
                "title":   option,
                "payload": option
            })
        message = {
            "attachment": {
                "type":    "template",
                "payload": {
                    "template_type": "button",
                    "text":          text,
                    "buttons":       buttons
                }
            }
        }
    else:
        message = {"text": text}

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params={"access_token": token},
                      data=json.dumps({
                          "recipient": {"id": recipient},
                          "message":   message
                      }),
                      headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)
