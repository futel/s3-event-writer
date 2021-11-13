
# merges two files
import s3_util

def merge(date):
    new_data_file = '{}.tmp'.format(date)
    s3_util.download_prod(date)
    existing_s3_file = '{}.original'.format(date)
    output = '{}.new'.format(date)
    return _merge(new_data_file, existing_s3_file, output)

def _merge(new_data_file, existing_s3_file, output):
    file1_content = _read_all(new_data_file)
    print('new from sqs = {} events'.format(len(file1_content)))
    file2_content = _read_all(existing_s3_file)
    print(' existing s3 = {} events'.format(len(file2_content)))
    content = file1_content + file2_content
    content = list(dict.fromkeys(content))
    print('      unique = {} events'.format(len(content)))
    content.sort()
    with open(output, 'w') as f:
        for line in content:
            f.write('{}\n'.format(line))
    return output

def _read_all(file):
    with open(file) as f:
        lines = f.readlines()
        return list(map(lambda x: x.rstrip(), lines))
