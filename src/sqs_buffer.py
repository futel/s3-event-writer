import os
import boto3
from botocore.config import Config
from msg_mapper import map_messages
from temp_files import buffer_to_file

# pulls messages from sqs and buffers them in date-based temp files

MAX_BLOCK_COUNT = 1000 # stop reading after this many messages

queue_url = os.environ.get('QUEUE_URL')
sqs = boto3.client('sqs', config=Config(region_name='us-west-2'))

def is_useful(msg):
    bad_types = ['Registry', 'PeerStatus']
    if msg['hostname'] != 'futel-prod.phu73l.net':
        return False
    if 'followme-operator' in msg['channel']:
        return False
    return False if msg['event'] in bad_types else True

# Reads a block of messages up to MAX_BLOCK_COUNT
def read_block():
    msg_count = 0
    useful_count = 0
    to_delete = []
    new_files = set()
    print('Reading messages from SQS...')
    while(msg_count < MAX_BLOCK_COUNT):
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
                useful_count += 1
            else:
                print('_', end='', flush=True)

            to_delete.append(msg['receipt_handle'])

            msg_count += 1
            if(msg_count % 80 == 0):
                print(' {}'.format(msg_count))

        # if(useful_count > 25): # ONLY FOR DEBUGGING TO NOT DRAIN QUEUE
        #     break

    return {
        'msg_count': msg_count,
        'to_delete': to_delete,
        'new_files': new_files
    }
