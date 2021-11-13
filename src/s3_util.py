
import boto3
import botocore

# helpers related to bucket mangling

BUCKET = 'logpublish'
s3 = boto3.resource('s3')

def make_prod_key(date):
    return 'events/prod/{}'.format(date)

# downloads a prod datestamp file to a file.
# if not exists, makes empty file
def download_prod(date):
    date = date.replace('-', '')
    key = make_prod_key(date)
    existing_file = '{}.original'.format(date)
    print('Downloading s3://{}{} from s3'.format(BUCKET, existing_file))
    try:
        s3.Bucket(BUCKET).download_file(key, existing_file)
    except botocore.exceptions.ClientError as e:
        # TODO: exception handling here is sketch, maybe check for key instead?
        print('New data for {} (no existing s3 data)'.format(date))
        open(existing_file, 'a')

def upload_file(date, file):
    key = make_prod_key(date)
    print('Uploading {} to s3://{}{}'.format(file, BUCKET, key))
    s3.Bucket(BUCKET).upload_file(file, key)
    print('Upload complete.')
