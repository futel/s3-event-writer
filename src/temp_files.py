import os
import re
import json
from msg_mapper import map_final

# helps with writing to temp files

# buffers the given message to a temp file
def buffer_to_file(msg):
    date = _get_date(msg)
    msg = map_final(msg)
    file = '{}.tmp'.format(date)
    with open(file, 'a') as f:
        f.write('{}\n'.format(json.dumps(msg)))
    return file

# gets the terse date string from a message timestamp
def _get_date(msg):
    timestamp = msg['timestamp']
    return re.sub(r'^(\d\d\d\d)-(\d\d)-(\d\d).*', r'\1\2\3', timestamp)
