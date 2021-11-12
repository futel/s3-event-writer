import json

# helps in mapping incoming messages to output messages

# converts to a more usable intermediate format
def map_messages(msgs):
    msgs = map(_parse_json_body, msgs)
    msgs = map(_convert_msg, msgs)
    return msgs

# converts intermediate format to output format
# output is simply timestamp, channel, event
def map_final(msg):
    return {
        'timestamp': msg['timestamp'],
        'channel': msg['channel'],
        'event': msg['event']
    }

def _convert_msg(msg):
    event = msg['Body']['Message']['event']
    eventName = event.get('UserEvent', event['Event'])
    return {
        'id': msg['MessageId'],
        'receipt_handle': msg['ReceiptHandle'],
        'timestamp': msg['Body']['Timestamp'],
        'hostname': msg['Body']['Message']['hostname'],
        'channel': event.get('Channel', ''),
        'event': eventName
    }

def _parse_json_body(msg):
    msg['Body'] = json.loads(msg['Body'])
    msg['Body']['Message'] = json.loads(msg['Body']['Message'])
    return msg
