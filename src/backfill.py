import sys
import boto3
import re
import json
import getopt
from botocore.config import Config

# takes "metrics" log data and backfills it into sns -> sqs

AWS_REGION='us-west-2'
DEFAULT_EVENT_HOSTNAME = 'futel-prod.phu73l.net'

arn = None
profile = 'default'
hostname = DEFAULT_EVENT_HOSTNAME

def usage():
    print('')
    print('Usage: ')
    print('')
    print('cat metrics.txt | python backfill.py <args>')
    print('')
    print(' where <args> are:\n')
    print('  -a <sns_arn>   : (required) provide the sns topic ARN')
    print('  -n <hostname>  : provide the hostname for these messages')
    print('                   (default = {})'.format(DEFAULT_EVENT_HOSTNAME))
    print('  -p <profile>   : use this aws profile name')
    print('  -h             : show usage')
    print('')
    sys.exit(1)

def line_to_message(line):
    fields = line.rstrip().split(' ')
    fields = map(lambda f: f.rstrip(','), fields)
    date, time, _, channel, _, event = fields
    time = re.sub(r',\d\d\d', '', time)
    channel = channel.replace('CHANNEL=', '')
    eventName = event.replace('name=', '')
    message = {}
    message['timestamp'] = f'{date}T{time}-08:00'
    message['hostname'] = hostname
    message['event'] = {
        'Event': 'UserEvent',
        'Channel': channel,
        'UserEvent': eventName,
        'Source': 'backfilling-data-hackity-hack'
    }
    return message

args,raw = getopt.getopt(sys.argv[1:], 'ha:n:p:', ['help', 'arn', 'hostname', 'profile'])
for arg,val in args:
    if arg in ('-h', '--help'):
        usage()
    if arg in ('-a', '--arn'):
        arn = val
    if arg in ('-p', '--profile'):
        profile = val
    if arg in ('-n', '--hostname'):
        hostname = val

if arn is None:
    print('\nError: arn is required')
    usage()

session = boto3.session.Session(profile_name=profile)
sns = session.client('sns', config=Config(region_name=AWS_REGION))

for line in sys.stdin:
    msg = line_to_message(line)
    print(msg);
    payload = json.dumps(msg)

    sns.publish(TopicArn=arn, Message=payload)
