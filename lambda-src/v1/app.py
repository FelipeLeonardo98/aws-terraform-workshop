from datetime import datetime
import time

def handler(event, context):
    time.sleep(5)
    return {
        "statusCode": 200,
        "body": {
            "message": "ok",
            "datetime": datetime.utcnow().isoformat(),
            "event": event
        }
    }