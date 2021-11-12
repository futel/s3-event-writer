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
to_delete = []
new_files = set()
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
            new_files.add(buffer_to_file(msg))
            print('!', end='', flush=True)
        else:
            print('_', end='', flush=True)

        to_delete.append(msg['receipt_handle'])

        msg_count += 1
        if(msg_count % 80 == 0):
            print(' {}'.format(msg_count))

    if(msg_count > 100):
        break

print('\nProcessed {} events from SQS'.format(msg_count))
print('Time to blend files into s3')
print(new_files)

# ...

print('Deleting {} handled messages from SQS...'.format(len(to_delete)))
for i,rcpt in enumerate(to_delete, start=1):
    res = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=rcpt)
    print('.', end='', flush=True)
    if(i % 80 == 0):
        print(' {}'.format(i))
