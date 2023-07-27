from unittest import mock, TestCase

import msg_mapper
import sqs_buffer

msg_asterisk = {'ReceiptHandle': 'xxx', 'MessageId': 'xxx', 'Body': {'Timestamp': 'xxx', 'Message': {"timestamp": "2023-07-26T19:48:18+00:00", "hostname": "futel-prod.phu73l.net", "event": {"Event": "UserEvent", "Privilege": "user,all", "Channel": "PJSIP/twilio-000012b0", "ChannelState": "6", "ChannelStateDesc": "Up", "CallerIDNum": "+15034448615", "CallerIDName": "ghost-mountain", "ConnectedLineNum": "<unknown>", "ConnectedLineName": "<unknown>", "Language": "en", "AccountCode": "", "Context": "robotron_ninth_position_play", "Exten": "i", "Priority": "1", "Uniqueid": "1690400891.5412", "Linkedid": "1690400891.5412", "UserEvent": "robotron_ninth_position_play"}}}}

msg_do = {'ReceiptHandle': 'xxx', 'MessageId': 'xxx', 'Body': {'Timestamp': 'xxx', 'Message': {"timestamp": "2023-07-26T19:49:18.695810", "hostname": "do-functions-prod", "event": {"Event": "UserEvent", "endpoint": "ghost-mountain", "Channel": "ghost-mountain", "UserEvent": "outgoing_dialstatus_completed_ghost-mountain"}}}}

class TestTest(TestCase):

    def test_convert_msg(self):
        self.assertEqual(
            msg_mapper._convert_msg(msg_asterisk),
            {'id': 'xxx',
             'receipt_handle': 'xxx',
             'timestamp': '2023-07-26T19:48:18+00:00',
             'hostname': 'futel-prod.phu73l.net',
             'channel': 'PJSIP/twilio-000012b0',
             'event': 'robotron_ninth_position_play'})
        self.assertEqual(
            msg_mapper._convert_msg(msg_do),
            {'id': 'xxx',
             'receipt_handle': 'xxx',
             'timestamp': '2023-07-26T19:49:18.695810',
             'hostname': 'do-functions-prod',
             'channel': 'ghost-mountain',
             'event': 'outgoing_dialstatus_completed_ghost-mountain'})

    def test_is_useful(self):
        self.assertTrue(
            sqs_buffer.is_useful(msg_mapper._convert_msg(msg_asterisk)))


if __name__ == '__main__':
    unittest.main()
