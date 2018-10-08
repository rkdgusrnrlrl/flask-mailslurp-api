import requests
import json
from email import message_from_string


class MailSlurpClient:
    API_KEY = ''

    def __init__(self, api_key=''):
        self.API_KEY = api_key

    def create_random_inbox(self):
        url = 'http://api.mailslurp.com/inboxes?apiKey=%s' % self.API_KEY
        dd = requests.post(url)

        data = json.loads(dd.content.decode())
        self.has_not_payload_raise_runtime_error(data)

        return data['payload']

    def get_inboxes(self):
        url = 'http://api.mailslurp.com/inboxes?apiKey=%s' % self.API_KEY
        response = requests.get(url)

        data = json.loads(response.content.decode())
        self.has_not_payload_raise_runtime_error(data)

        return data['payload']

    def get_messages(self, inbox_id):
        url = 'http://api.mailslurp.com/inboxes/%s?apiKey=%s' % (inbox_id , self.API_KEY)
        response = requests.get(url)

        data = json.loads(response.content.decode())
        self.has_not_payload_raise_runtime_error(data)

        return data['payload']
        # data_res_messages['payload'][0]['body']

    @staticmethod
    def get_eamil_text_contents(email_string):
        msg = message_from_string(email_string)

        if msg.is_multipart():
            html = None
            for part in msg.get_payload():

                print("%s, %s" % (part.get_content_type(), part.get_content_charset()))


                if part.get_content_charset() is None:
                    # We cannot know the character set, so return decoded "something"
                    text = part.get_payload(decode=True)
                    continue

                charset = part.get_content_charset()

                if part.get_content_type() == 'text/plain':
                    text = part.get_payload(decode=True).decode('utf-8')

                if part.get_content_type() == 'text/html':
                    html = part.get_payload(decode=True).decode('utf-8')

            if text is not None:
                return text.strip()
            else:
                return html.strip()
        else:
            return msg.get_payload(decode=True).decode('utf-8')



    @staticmethod
    def has_not_payload_raise_runtime_error(dd):
        if not 'payload' in dd:
            raise Exception(dd['message'])