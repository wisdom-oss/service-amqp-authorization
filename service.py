"""AMQP Authorization Service"""
import asyncio
import logging
import sys

import amqp_rpc_server
import pydantic.error_wrappers

import server_functions
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
    _amqp_settings.dsn.port = 5672 if _amqp_settings.dsn.port is None else _amqp_settings.dsn.port
    # Check the connectivity to the message broker
    _message_broker_available = asyncio.run(
        tools.is_host_available(
            host=_amqp_settings.dsn.host,
            port=_amqp_settings.dsn.port
        )
    )
    if not _message_broker_available:
        logging.critical('The specified message broker (Host: %s | Port: %s) is not reachable',
                         _amqp_settings.dsn.host, _amqp_settings.dsn.port)
        sys.exit(1)
    # = Read the database connection settings and check the database connectivity =
    try:
        _db_settings = settings.DatabaseSettings()
    except pydantic.error_wrappers.ValidationError as config_error:
        logging.critical('Unable to read the settings for the connection to the database',
                         exc_info=config_error)
        sys.exit(1)
    logging.debug('Successfully read the settings for the database connection:\n%s',
                  _db_settings.json(indent=2, by_alias=True))
    # Set the port of the database if it is not set currently
    _db_settings.dsn.port = 3306 if _db_settings.dsn.port is None else _db_settings.dsn.port
    # Check the connectivity to the database
    _database_available = asyncio.run(
        tools.is_host_available(
            _db_settings.dsn.host,
            _db_settings.dsn.port
        )
    )
    if not _database_available:
        logging.critical('The specified database (Host: %s | Port: %s) is not reachable',
                         _db_settings.dsn.host, _db_settings.dsn.port)
        sys.exit(1)
    logging.info('Passed all pre-startup checks and all dependent services are reachable')
    logging.info('Starting the AMQP Server')
    amqp_server = amqp_rpc_server.Server(
        amqp_dsn=_amqp_settings.dsn,
        exchange_name=_amqp_settings.exchange_name,
        content_validator=server_functions.content_validator,
        executor=server_functions.executor
    )
    # Start the server
    amqp_server.start_server()
    # TODO: Loop via events until shutdown signal is received
