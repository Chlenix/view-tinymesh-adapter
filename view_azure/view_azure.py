import base64

from azure.eventhub import EventHubClient, Sender, EventData

import logging
import config
import json


class ViewAzureClient:
    def __init__(self):
        self.sas_key = config.ENV['AZURE_SAS_KEY']
        self.sas_user = config.ENV['AZURE_SAS_USER']

        self.logger = logging.getLogger('azure')
        self.logger.setLevel('DEBUG')

        self.client = None
        self.sender = None

    def run(self):
        self.client = EventHubClient.from_connection_string(
            'Endpoint=%s;SharedAccessKeyName=%s;SharedAccessKey=%s;EntityPath=%s'
            % (config.AZURE['ENDPOINT'], self.sas_user, self.sas_key, config.AZURE['ENTITY_PATH'])
        )
        self.sender = self.client.add_sender(partition='0')

        # client.run() returns a 'failed' boolean
        return not self.client.run()

    def stop(self):
        self.client.stop()

    def publish(self, message):
        key = message['key'].split('-', 4)[-1]

        _, device_id = base64.b64decode(key).decode('ascii').split('/')

        body = message['proto/tm']

        devices = []

        for formatting_rule in config.FORMAT.values():
            # prepare the lambda function which converts the raw value to unit value
            convert_to_unit = formatting_rule['conversion_fn']

            # build the device body
            device = {
                'deviceid': device_id,
                'property': formatting_rule['property_name'],
                'unit': formatting_rule['unit'],
                'values': [],
            }

            # get the raw value recorded in the sensor
            raw_value = body[formatting_rule['key_name']]

            # convert the value to unit value
            value = {
                'starttime': message['received'],
                'value': convert_to_unit(raw_value),
            }

            # append the value to the device object
            device['values'].append(value)

            # add the device dict to the array of devices
            devices.append(device)

        # send devices object to Azure server
        event = {'devices': devices}
        response = self.sender.send(EventData(str(event)))
        print(device_id + ':\n\n' + response.name)
