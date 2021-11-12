import os
import boto3
from msg_mapper import map_messages
from temp_files import buffer_to_file

# pulls messages from sqs and buffers them in date-based temp new_files

queue_url = os.environ.get('QUEUE_URL')
sqs = boto3.client('sqs');

def is_useful(msg):
    bad_types = ['Registry', 'PeerStatus']
    if msg['hostname'] != 'futel-prod.phu73l.net':
        return False
    return False if msg['event'] in bad_types else True

# Reads all remaining SQS messages into date named temp files
def read_everything():
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

        if(msg_count > 100): # ONLY FOR DEBUGGING!
            break

    return {
        'msg_count': msg_count,
        'to_delete': to_delete,
        'new_files': new_files
    }
