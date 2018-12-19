import logging

ENV = {
    'AZURE_SAS_KEY': '',
    'AZURE_SAS_USER': '',
    'TINYM_USERNAME': '',
    'TINYM_PASSWORD': '',
}

AZURE = {
    'ENDPOINT': 'sb://test-view.servicebus.windows.net/',
    'ENTITY_PATH': 'dank-single-eventhub',
    'PARTITION': '0',
}

TINYM = {
    'BASE_URL': 'https://cloud.tiny-mesh.com',
    'API_VERSION': 'v2',
    'NETWORK_ID': 'SHR',
}

FORMAT = {
    'HUMIDITY': {
        'property_name': 'ActualRelativeHumidity',
        'unit': 'Percent',
        'key_name': 'locator',
        'conversion_fn': lambda x: ((x >> 16) / 16382) * 100,
    },
    'TEMPERATURE': {
        'property_name': 'ActualTemperature',
        'unit': 'C',
        'key_name': 'locator',
        'conversion_fn': lambda x: (((((x & 65535) / 4) / 16382) * 165) - 40)
    },
    'CO2': {
        'property_name': 'ActualCO2',
        'unit': 'ppm',
        'key_name': 'msg_data',
        'conversion_fn': lambda x: x
    }
}

LOGGING = {
    'LEVEL': logging.INFO,
    'FORMAT': '[%(asctime)s] - (%(levelname)s): %(message)s',
    'REL_LOG_DIR': 'logs',
}