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

    def subscribe(self):
        url = '%s/%s/%s/%s' % (self.BASE_URL, self.VERSION, 'messages', 'SHR')

        params = {
            'query': '',
            'stream': 'true',
            'continuous': 'true',
            'date.from': 'NOW',
        }

        response = self.s.get(url=url, params=params, stream=True)

        if response.status_code == status_codes.OK:
            for chunk in response.iter_content(self.CHUNK_SIZE):
                message = json.loads(chunk)
                if 'meta' not in message:
                    yield message
        else:
            return False
