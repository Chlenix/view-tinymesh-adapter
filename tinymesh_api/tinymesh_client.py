import requests

from requests.auth import HTTPBasicAuth
from requests.status_codes import codes as status_codes

import json
import logging
import config


class TinyMeshClient:

    def __init__(self):
        self.s = requests.session()
        self.s.auth = HTTPBasicAuth(config.ENV['TINYM_USERNAME'], config.ENV['TINYM_PASSWORD'])

        self.BASE_URL = config.TINYM['BASE_URL']
        self.VERSION = config.TINYM['API_VERSION']

        self.CHUNK_SIZE = 8096
        self.NETWORK_ID = config.TINYM['NETWORK_ID']

    def subscribe(self):
        url = '%s/%s/%s/%s' % (self.BASE_URL, self.VERSION, 'messages', self.NETWORK_ID)

        params = {
            'query': '',
            'stream': 'true',
            'continuous': 'true',
            'date.from': 'NOW',
        }

        response = self.s.get(url=url, params=params, stream=True)

        if response.status_code == status_codes.OK:
            for chunk in response.iter_content(self.CHUNK_SIZE):

                logging.info('Message received from network id \'%s\' (length: %d bytes)', self.NETWORK_ID, len(chunk))

                # convert message to json
                message = json.loads(chunk)

                if 'meta' not in message:
                    # if the message is not meta, it contains sensor readings
                    yield message
                else:
                    # otherwise it is the first message from the server
                    logging.info('Successfully subscribed to Tinymesh network \'%s\'', self.NETWORK_ID)
        else:
            # status code is not 200
            logging.error('Tinymesh Cloud responded with status %d', response.status_code)
            body = json.loads(response.text)
            if 'error' in body:
                # attach the error message from the server (if any)
                logging.error('Error message: %s', body['error'])

            return False
