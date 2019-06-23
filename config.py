import logging
import math

ENV = {
    'AZURE_SAS_KEY': '',
    'AZURE_SAS_USER': '',
    'TINYM_USERNAME': '',
    'TINYM_PASSWORD': '',
}

AZURE = {
    # 'ENDPOINT': 'sb://invadeeh.servicebus.windows.net/',
    'ENDPOINT': 'sb://eh-esmartflex-dev-statsbygg.servicebus.windows.net/',
    'ENTITY_PATH': 'iotexternaleh',
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
        'check_bad_fn': lambda x: x == 0
    },
    'TEMPERATURE': {
        'property_name': 'ActualTemperature',
        'unit': 'C',
        'key_name': 'locator',
        'conversion_fn': lambda x: (((((x & 65535) / 4) / 16382) * 165) - 40),
        'check_bad_fn': lambda x: x < 0
    },
    'CO2': {
        'property_name': 'ActualCO2',
        'unit': 'ppm',
        'key_name': 'msg_data',
        'conversion_fn': lambda x: x,
        'check_bad_fn': lambda x: not (100 < x < 8000),
    },
    'LIGHT': {
        'property_name': 'LightStrengthReading',
        'unit': 'Lux',
        'key_name': 'analog_io_0',
        'conversion_fn': lambda x: math.pow(10, x * 0.0015658),
        'check_bad_fn': lambda x: False,
    },
    'NOISE': {
        'property_name': 'SoundLevelReading',
        'unit': 'dB',
        'key_name': 'analog_io_1',
        'conversion_fn': lambda x: (90 - (30 * (x / 2048))),
        'check_bad_fn': lambda x: False,
    },
    'MOVEMENT': {
        'property_name': 'MotionDetectedReading',
        'unit': 'motion',
        'key_name': 'digital_io_5',
        'conversion_fn': lambda x: x,
        'check_bad_fn': lambda x: False,
    },
}

LOGGING = {
    'LEVEL': logging.WARNING,
    'FORMAT': '[%(asctime)s] - (%(levelname)s): %(message)s',
    'REL_LOG_DIR': 'logs',
}
