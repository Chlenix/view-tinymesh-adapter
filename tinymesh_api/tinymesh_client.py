import requests

from requests.auth import HTTPBasicAuth
from requests.status_codes import codes as status_codes

from requests.exceptions import ChunkedEncodingError, ContentDecodingError, ConnectionError, StreamConsumedError

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

        self.KEEP_ALIVE = '\r\n'

    def __loop_messages(self, response):
        pass

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
            try:
                for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE, decode_unicode=True):

                    logging.info('Message received from network id \'%s\' (length: %d bytes)', self.NETWORK_ID,
                                 len(chunk))

                    # decode bytes
                    # chunk_str = chunk.decode('utf-8')

                    if chunk == self.KEEP_ALIVE:
                        # ignore the keep-alive message
                        continue

                    # convert message to json
                    try:
                        message = json.loads(chunk)
                    except json.decoder.JSONDecodeError:
                        logging.error('Unexpected format, could not decode json. Skipping message...')
                        continue

                    if 'meta' not in message:
                        # if the message is not meta, it contains sensor readings
                        yield message
                    else:
                        # otherwise it is the first message from the server
                        logging.info('Successfully subscribed to Tinymesh network \'%s\'', self.NETWORK_ID)

            except (ConnectionError, ChunkedEncodingError, ContentDecodingError, StreamConsumedError) as err:
                logging.error('Failed iterating over a chunk. Error: %s', err)

            except TypeError as err:
                logging.error('TypeError occurred when iterating over a chunk: %s', err)

        else:
            # status code is not 200
            logging.error('Tinymesh Cloud responded with status %d', response.status_code)
            body = json.loads(response.text)

            if 'error' in body:
                # attach the error message from the server (if any)
                logging.error('Error message: %s', body['error'])
