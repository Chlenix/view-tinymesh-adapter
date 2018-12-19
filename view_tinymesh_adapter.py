import os
import logging
import config
import datetime

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


def setup_logging():

    filename_fmt = '%s.log' % datetime.date.today()

    logging.basicConfig(
        filemode='a+',
        filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), config.LOGGING['REL_LOG_DIR'], filename_fmt),
        format=config.LOGGING['FORMAT'],
        level=config.LOGGING['LEVEL'],
    )


def setup():
    setup_logging()
    setup_env()


if __name__ == '__main__':
    setup()

    tinymesh_client = TinyMeshClient()

    view_client = ViewAzureClient()
    if not view_client.run():
        exit(1)

    try:
        for message in tinymesh_client.subscribe():
            view_client.publish(message)
    except KeyboardInterrupt:
        logging.warning('Keyboard interrupt received. Stopping...')
    finally:
        view_client.stop()

