
# merges two files
import s3_util

def merge(date):
    print('here')
    file1 = '{}.tmp'.format(date)
    s3_util.download_prod(date)
    file2 = '{}.original'.format(date)
    output = '{}.new'.format(date)
    return _merge(file1, file2, output)

def _merge(file1, file2, output):
    file1_content = _read_all(file1)
    print('file1 = {} records'.format(len(file1_content)))
    file2_content = _read_all(file2)
    print('file2 = {} records'.format(len(file2_content)))
    content = file1_content + file2_content
    content = list(dict.fromkeys(content))
    print('unique: {}'.format(len(content)))
    content.sort()
    with open(output, 'w') as f:
        for line in content:
            f.write('{}\n'.format(line))
    return output

def _read_all(file):
    with open(file) as f:
        lines = f.readlines()
        return list(map(lambda x: x.rstrip(), lines))
