import os
import boto3
import sqs_buffer

queue_url = os.environ.get('QUEUE_URL')
sqs = boto3.client('sqs');

state = sqs_buffer.read_everything()

print('\nProcessed {} events from SQS'.format(state['msg_count']))
print('Time to blend files into s3')
print(state['new_files'])

# ...

print('Deleting {} handled messages from SQS...'.format(len(state['to_delete'])))
for i,rcpt in enumerate(state['to_delete'], start=1):
    res = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=rcpt)
    print('.', end='', flush=True)
    if(i % 80 == 0):
        print(' {}'.format(i))
