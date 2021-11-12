import os
import boto3
from msg_mapper import map_messages
import json

queue_url = os.environ.get('QUEUE_URL')

sqs = boto3.client('sqs');

def is_useful(msg):
    bad_types = ['Registry', 'PeerStatus']
    print(msg)
    if msg['hostname'] != 'futel-prod.phu73l.net':
        return False
    return False if msg['event']['Event'] in bad_types else True

while(True):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )
    msgs = response.get("Messages", [])
    if len(msgs) == 0:
        # empty message batch -- all done
        break

    # msgs = filter(is_useful, msgs)
    msgs = map_messages(msgs)

    for msg in msgs:
        print(json.dumps(msg, indent=2))
        # host = msg['hostname']

    break # JUST FOR DEBUGGING!!
