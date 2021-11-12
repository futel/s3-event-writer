import os
import boto3
from msg_mapper import map_messages
from temp_files import buffer_to_file
import json

queue_url = os.environ.get('QUEUE_URL')

sqs = boto3.client('sqs');

def is_useful(msg):
    bad_types = ['Registry', 'PeerStatus']
    if msg['hostname'] != 'futel-prod.phu73l.net':
        return False
    return False if msg['event'] in bad_types else True

msg_count = 0
while(True):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )
    msgs = response.get("Messages", [])
    if len(msgs) == 0:
        print('\nNo more new messages found. All done.')
        break

    msgs = map_messages(msgs)
    msgs = filter(is_useful, msgs)

    for msg in msgs:
        buffer_to_file(msg)
        print('.', end='')
        msg_count += 1
        if(msg_count % 50 == 0):
            print('')

    if(msg_count > 100):
        break
