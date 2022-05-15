"""A collection of tools which are used multiple times in this service"""
import asyncio
import datetime
import logging

import database
import database.crud
import enums
import models.requests
import models.responses

_logger = logging.getLogger(__name__)


async def is_host_available(host: str, port: int, timeout: float = 10.0) -> bool:
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
            asyncio.open_connection(host, port), timeout=timeout
        )
        # Close the writer and wait until it is closed
        _writer.close()
        await _writer.wait_closed()
        return True
    except:  # pylint: disable=bare-except
        return False


def format_timestamp(t: float):
    return datetime.datetime.fromtimestamp(t).strftime("%A %d.%m.%Y %H:%M:%s")


def run_token_introspection(
    request: models.requests.TokenValidationData,
) -> models.responses.TokenIntrospection:
    """
    Run a new token introspection for the supplied request

    :param request: The request data
    :type request: models.incoming.ValidateTokenRequest
    :return:
    :rtype:
    """
    # Get information about the two possible token types
    access_token_information = database.crud.get_access_token_data(request.token)
    if access_token_information is None:
        return models.responses.TokenIntrospection(
            active=False, reason=enums.TokenIntrospectionFailure.INVALID_TOKEN
        )
    if datetime.datetime.now() > access_token_information.expires:
        return models.responses.TokenIntrospection(
            active=False, reason=enums.TokenIntrospectionFailure.EXPIRED
        )
    if datetime.datetime.now() < access_token_information.created:
        return models.responses.TokenIntrospection(
            active=False, reason=enums.TokenIntrospectionFailure.TOKEN_USED_TOO_EARLY
        )
    # Get the information about the user account
    user = database.crud.get_user_account(access_token_information.owner_id)
    if user is None:
        return models.responses.TokenIntrospection(
            active=False, reason=enums.TokenIntrospectionFailure.NO_USER_ASSOCIATED
        )
    if not user.active:
        return models.responses.TokenIntrospection(
            active=False, reason=enums.TokenIntrospectionFailure.USER_DISABLED
        )
    # Get the scopes of the access token
    access_token_scopes = database.crud.get_access_token_scopes(access_token_information)
    if request.scopes is not None:
        required_scopes = set(sorted(request.scopes))
        available_scopes = set(sorted([scope.scope_string_value for scope in access_token_scopes]))
        if not required_scopes.issubset(available_scopes):
            return models.responses.TokenIntrospection(
                active=False, reason=enums.TokenIntrospectionFailure.MISSING_PRIVILEGES
            )
    user = models.responses.UserAccount(**user.dict())
    return models.responses.TokenIntrospection(
        active=True,
        scope=request.scopes,
        token_type="access_token",
        expires_at=access_token_information.expires.timestamp(),
        created_at=access_token_information.created.timestamp(),
        user=user,
    )
