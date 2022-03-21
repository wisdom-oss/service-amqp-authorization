"""AMQP Authorization Service"""
import asyncio
import logging
import sys
import typing

import pydantic.error_wrappers
from pipfile import Pipfile
import amqp_rpc_server

import settings
import tools


if __name__ == '__main__':
    # Read the service settings and configure the logging
    _service_settings = settings.ServiceSettings()
    logging.basicConfig(
        format=_service_settings.log_format,
        level=_service_settings.log_level.upper()
    )
    logging.info('Starting the "%s" service', _service_settings.name)
    # Get the current event loop
    _loop = asyncio.get_event_loop()
    # = Read the AMQP Settings and check the server connection =
    try:
        _amqp_settings = settings.AMQPSettings()
    except pydantic.error_wrappers.ValidationError as config_error:
        logging.critical('Unable to read the settings for the connection to the message broker',
                         exc_info=config_error)
        sys.exit(1)
    # Now check the connection to the message broker
    logging.debug('Successfully read the settings for the message broker connection:\n%s',
                  _amqp_settings.json(indent=2, by_alias=True))
    # Set the port if it is None
    _amqp_settings.dsn.port = 5762 if _amqp_settings.dsn.port is None else _amqp_settings.dsn.port
    # Check the connectivity to the message broker
    _message_broker_available = _loop.run_until_complete(
        tools.is_host_available(
            host=_amqp_settings.dsn.host,
            port=_amqp_settings.dsn.port
        )
    )
    if not _message_broker_available:
        logging.critical('The specified message broker (Host: %s | Port: %s) is not reachable',
                         _amqp_settings.dsn.host, _amqp_settings.dsn.port)
        sys.exit(1)
