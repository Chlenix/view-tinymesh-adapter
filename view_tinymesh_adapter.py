import os
import logging
import config

from tinymesh_api import TinyMeshClient
from view_azure import ViewAzureClient


def setup_env():
    # Environment
    config.ENV['AZURE_SAS_KEY'] = os.environ.get('AZURE_SAS_KEY', None)
    config.ENV['AZURE_SAS_USER'] = os.environ.get('AZURE_SAS_USER', None)
    config.ENV['TINYM_USERNAME'] = os.environ.get('TINYM_USERNAME', None)
    config.ENV['TINYM_PASSWORD'] = os.environ.get('TINYM_PASSWORD', None)

    for key, value in config.ENV.items():
        if value is None or value == '':
            raise ValueError('%s environment variable is required but not set.' % key)


if __name__ == '__main__':
    setup_env()

    viewClient = ViewAzureClient()
    if not viewClient.run():
        exit(1)

    tinyMeshClient = TinyMeshClient()

    for message in tinyMeshClient.subscribe():
        viewClient.publish(message)

    viewClient.stop()
