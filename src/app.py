import os
import boto3
import sqs_buffer
import file_blender
import s3_util

queue_url = os.environ.get('QUEUE_URL')

state = sqs_buffer.read_everything()

print('\nProcessed {} events from SQS'.format(state['msg_count']))
print('Time to blend files into s3')

for file in state['new_files']:
    date = file.replace('.tmp', '')
    outfile = file_blender.merge(date)
    s3_util.upload_file(date, outfile)
    for suffix in ['tmp', 'original', 'new']:
        f = '{}.{}'.format(date, suffix)
        os.remove(f)
        print('remove {}'.format(f))


print('Deleting {} handled messages from SQS...'.format(len(state['to_delete'])))
sqs = boto3.client('sqs')
for i,rcpt in enumerate(state['to_delete'], start=1):
    res = sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=rcpt)
    print('.', end='', flush=True)
    if(i % 80 == 0):
        print(' {}'.format(i))
