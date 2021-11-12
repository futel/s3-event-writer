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
print('Reading messages from SQS...')
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

    for msg in msgs:
        if(is_useful(msg)):
            buffer_to_file(msg)
            print('!', end='', flush=True)
        else:
            print('_', end='', flush=True)

        res = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=msg['receipt_handle'])
        print('.', end='', flush=True)

        msg_count += 1
        if(msg_count % 40 == 0):
            print(' {}'.format(msg_count))

    if(msg_count > 300):
        break

print('\nProcessed {} events from SQS'.format(msg_count))
