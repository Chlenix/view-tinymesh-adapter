import base64

from azure.eventhub import EventHubClient, Sender, EventData
from azure.eventhub.common import EventHubError

import logging
import config
import json


class ViewAzureClient:
    def __init__(self):
        self.SAS_KEY = config.ENV['AZURE_SAS_KEY']
        self.SAS_USER = config.ENV['AZURE_SAS_USER']

        self.ENTITY_PATH = config.AZURE['ENTITY_PATH']
        self.ENDPOINT = config.AZURE['ENDPOINT']
        self.PARTITION = config.AZURE['PARTITION']

        self.client = None
        self.sender = None

    def run(self):
        self.client = EventHubClient.from_connection_string(
            'Endpoint=%s;SharedAccessKeyName=%s;SharedAccessKey=%s;EntityPath=%s'
            % (self.ENDPOINT, self.SAS_USER, self.SAS_KEY, self.ENTITY_PATH)
        )
        self.sender = self.client.add_sender(partition=self.PARTITION)

        # client.run() returns a 'failed' boolean

        status = False

        try:
            status = not self.client.run()
        except EventHubError as e:
            logging.error(str(e))
        finally:
            return status

    def stop(self):
        self.client.stop()
        logging.warning('Azure Client has been stopped')

    def publish(self, message):
        key = message['key'].split('-', 4)[-1]

        _, device_id = base64.b64decode(key).decode('ascii').split('/')

        body = message['proto/tm']

        devices = []

        for formatting_rule in config.FORMAT.values():
            # prepare the lambda function which converts the raw value to unit value
            convert_to_unit = formatting_rule['conversion_fn']

            property_name = formatting_rule['property_name']
            unit = formatting_rule['unit']

            # build the device body
            device = {
                'deviceid': device_id,
                'property': property_name,
                'unit': unit,
                'values': [],
            }

            # get the raw value recorded in the sensor
            selector = formatting_rule['key_name']
            if selector not in body:
                # skip a property if the sensor did not contain the necessary key
                logging.warning('Device \'%s\' missing key \'%s\' for reading \'%s\'. \'%s\' will therefore be skipped',
                                device_id, selector, property_name, property_name)

                continue

            raw_value = body[selector]

            # convert the value to unit value
            value = {
                'starttime': message['received'],
                'value': convert_to_unit(raw_value),
            }

            # append the value to the device object
            device['values'].append(value)

            # add the device dict to the array of devices
            devices.append(device)

        # convert to string with correct json format
        event_message = json.dumps({'devices': devices})

        logging.info('Device \"%s\" publishing event to EventHub \"%s\" (message length: %d bytes)',
                     device_id, self.ENTITY_PATH, len(event_message))

        # send devices object to Azure server
        response = self.sender.send(EventData(event_message))

        logging.info('EventHub \"%s\" responded with status %s.', self.ENTITY_PATH, response.name)
