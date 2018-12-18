import base64

from azure.eventhub import EventHubClient, Sender, EventData

import logging
import config


class ViewAzureClient:
    def __init__(self):
        self.sas_key = config.ENV['AZURE_SAS_KEY']
        self.sas_user = config.ENV['AZURE_SAS_USER']

        self.logger = logging.getLogger('azure')
        self.logger.setLevel('DEBUG')

        self.client = None
        self.sender = None

    def run(self):
        try:
            self.client = EventHubClient.from_connection_string(
                'Endpoint=%s;SharedAccessKeyName=%s;SharedAccessKey=%s;EntityPath=%s'
                % (config.AZURE['ENDPOINT'], self.sas_user, self.sas_key, config.AZURE['ENTITY_PATH'])
            )
            self.sender = self.client.add_sender(partition='0')
            self.client.run()
        except:
            pass

    def stop(self):
        if self.client is not None:
            try:
                self.client.stop()
            except:
                pass

    def convert_and_send(self, message):

        key = message['key'].split('-', 4)[-1]
        nid, device = base64.b64decode(key).decode('ascii').split('/')

        response = self.sender.send(EventData(str(message)))
        print(response)
