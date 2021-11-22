import json

# helps in mapping incoming messages to output messages

# converts to a more usable intermediate format
def map_message(msg):
    msg = _parse_json_body(msg)
    return _convert_msg(msg)

def map_messages(msgs):
    return map(map_message, msgs)

# converts intermediate format to output format
# output is simply timestamp, channel, event
def map_final(msg):
    return {
        'timestamp': msg['timestamp'],
        'channel': msg['channel'],
        'event': msg['event']
    }

def _convert_msg(msg):
    # print(json.dumps(msg, indent=2))
    event = msg['Body']['Message']['event']
    eventName = event.get('UserEvent', event['Event'])
    # Use the timestamp from the message body, fall back to the sqs body
    bodyTimestamp = msg['Body']['Timestamp']
    timestamp = msg['Body']['Message'].get('timestamp', bodyTimestamp)
    return {
        'id': msg['MessageId'],
        'receipt_handle': msg['ReceiptHandle'],
        'timestamp': timestamp,
        'hostname': msg['Body']['Message']['hostname'],
        'channel': event.get('Channel', ''),
        'event': eventName
    }

def _parse_json_body(msg):
    msg['Body'] = json.loads(msg['Body'])
    msg['Body']['Message'] = json.loads(msg['Body']['Message'])
    return msg
