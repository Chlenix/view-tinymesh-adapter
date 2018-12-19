# View-TinyMesh Adapter

## Requirements
Python 3.6+

Dependencies:
`pip install -r requirements.txt`

## Configuration

Script configuration file: `config.py`

In it, fill out the following fields:
##### Azure
    
    'ENDPOINT': 'sb://<YOUR-VIEW>.servicebus.windows.net/',
    'ENTITY_PATH': '<EVENTHUB>',
    'PARTITION': '0'

##### Environment Variables
Designed to work with environment variables, but can also be filled out directly in the config file.

    'AZURE_SAS_KEY':  Azure SAS key
    'AZURE_SAS_USER': Azure SAS user
    'TINYM_USERNAME': TinyMesh cloud username for basic auth
    'TINYM_PASSWORD': TinyMesh cloud password for basic auth
