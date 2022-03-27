"""A collection of tools which are used multiple times in this service"""
import asyncio
import datetime
import logging
import time

import database
import database.crud
import enums
import models.incoming
import models.responses

_logger = logging.getLogger(__name__)


async def is_host_available(
        host: str,
        port: int,
        timeout: float = 10.0
) -> bool:
    """
    Check if the specified host is reachable on the specified port.
    
    :param host: The hostname or ip-address of the service that shall be checked
    :type host: str
    :param port: The port of the service which shall be checked
    :type port: int
    :param timeout: The time that is waited until the operation times out
    :type timeout: float
    :return: ``True`` if the host is reachable on the specified port
    :rtype: bool
    """
    try:
        # Try opening a stream to the specified host and port
        _reader, _writer = await asyncio.wait_for(
            asyncio.open_connection(
                host,
                port
            ), timeout=timeout
        )
        # Close the writer and wait until it is closed
        _writer.close()
        await _writer.wait_closed()
        return True
    except:  # pylint: disable=bare-except
        return False


def format_timestamp(t: float):
    return datetime.datetime.fromtimestamp(t).strftime('%A %d.%m.%Y %H:%M:%s')


def run_token_introspection(request: models.incoming.ValidateTokenRequest) -> \
        models.responses.TokenIntrospectionResult:
    """
    Run a new token introspection for the supplied request
    
    :param request: The request data
    :type request: models.incoming.ValidateTokenRequest
    :return:
    :rtype:
    """
    _logger.info('Running a new token introspection')
    _logger.debug('Introspection Request Data:\n%s', request.json(indent=2))
    # Try to get a token from the database
    session = next(database.session())
    try:
        access_token = database.crud.get_access_token(request.oauth2_token, session)
    except ValueError:
        _logger.info('The supplied token was not found in the database')
        return models.responses.TokenIntrospectionResult(
            is_active=False,
            error_reason=enums.TokenIntrospectionFailure.NO_TOKEN_FOUND
        )
    # Since a token was found now check that the token is not expired
    if time.time() >= access_token.expires_at:
        _logger.info('The supplied token is expired.\n'
                     'Current Time: %s\n'
                     'Token Expiration Time: %s',
                     format_timestamp(time.time()),
                     format_timestamp(access_token.expires_at))
        return models.responses.TokenIntrospectionResult(
            is_active=False,
            error_reason=enums.TokenIntrospectionFailure.TOKEN_EXPIRED
        )
    # Since the token is not expired check if the token is used before its creation time
    if time.time() <= access_token.created_at:
        _logger.critical('The supplied token is used before its creation time.\n'
                         'Current Time: %s\n'
                         'Token Expiration Time: %s',
                         format_timestamp(time.time()),
                         format_timestamp(access_token.expires_at))
        return models.responses.TokenIntrospectionResult(
            is_active=False,
            error_reason=enums.TokenIntrospectionFailure.TOKEN_USED_BEFORE_CREATION
        )
    # Get a list of all scopes assigned to the token
    _logger.debug('Generating list of all scopes assigned to the token')
    token_scopes = [scope.oauth2_value for scope in access_token.scopes]
    _logger.debug('List of all scopes assigned to the token: %s', token_scopes)
    # Check if the token has admin access
    if "admin" in token_scopes:
        _logger.info('The supplied token is valid for the specified scope')
        return models.responses.TokenIntrospectionResult(
            is_active=True,
            scopes=["admin", request.oauth2_scope],
            token_type=enums.TokenType.ACCESS_TOKEN,
            expires_at=access_token.expires_at,
            created_at=access_token.created_at
        )
    if request.oauth2_scope in token_scopes:
        _logger.info('The supplied token is valid for the specified scope')
        return models.responses.TokenIntrospectionResult(
            is_active=True,
            scopes=[request.oauth2_scope],
            token_type=enums.TokenType.ACCESS_TOKEN,
            expires_at=access_token.expires_at,
            created_at=access_token.created_at
        )
    # Since the token did not have to fitting scope return an error
    _logger.info('The supplied token is not valid for the supplied scope')
    return models.responses.TokenIntrospectionResult(
        is_active=False,
        error_reason=enums.TokenIntrospectionFailure.INSUFFICIENT_SCOPE
    )
