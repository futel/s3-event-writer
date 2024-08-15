import os
import boto3
from botocore.config import Config
from msg_mapper import map_messages
from temp_files import buffer_to_file

# pulls messages from sqs and buffers them in date-based temp files

MAX_BLOCK_COUNT = 1000 # stop reading after this many messages
PROD_HOSTS = [
    'futel-prod.phu73l.net',    # Prod asterisk.
    'futel-prod-back',          # Previous prod asterisk during promotion.
    'dialplan-functions-prod']  # Dialplan for twilio pv.

queue_url = os.environ.get('QUEUE_URL')
sqs = boto3.client('sqs', config=Config(region_name='us-west-2'))

invalids = dict()
invalids['hostname'] = dict()
invalids['channel'] = dict()
invalids['event'] = dict()

def _track_invalid(what, content):
    if content in invalids[what]:
        invalids[what][content] = invalids[what][content] + 1
    else:
        invalids[what][content] = 1
    return False

def print_invalid():
    if len(invalids['hostname']) + len(invalids['channel']) + len(invalids['event']) == 0:
        print("All messages were useful. Awesome!")
        return
    print("Here is what was not useful/ignored:")
    print(invalids)

def is_useful(msg):
    """
    If msg is useful, return True, else add it to the invalids collection.
    """
    # Messages come from several sources and the format is largely historical
    # cruft, so we toss what we don't understand as well as what we know we
    # don't want.
    bad_types = ['Registry', 'PeerStatus', None]
    if msg['hostname'] not in PROD_HOSTS:
        return _track_invalid('hostname', msg['hostname'])
    if 'followme-operator' in msg.get('channel'):
        return _track_invalid('channel', msg.get('channel'))
    if msg.get('event') in bad_types:
        return _track_invalid('event', msg.get('event'))
    return True

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
