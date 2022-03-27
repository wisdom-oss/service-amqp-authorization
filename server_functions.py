"""The module containing functions for the AMQP server"""
import json
import logging

import pydantic.error_wrappers

import database.crud
import database.tables
import models.incoming
import models.responses
import tools

_content_validation_logger = logging.getLogger('content_validation')
_executor_logger = logging.getLogger('executor')


def content_validator(message: bytes) -> bool:
    """Check if the content is parseable into the incoming request model"""
    try:
        models.incoming.IncomingRequest.parse_obj({"payload": json.loads(message)})
        return True
    except pydantic.error_wrappers.ValidationError as e:
        _content_validation_logger.critical('Rejected message', exc_info=e)
        return False
    

def executor(message: bytes) -> bytes:
    """Parse the message again and run the appropriate action"""
    _executor_logger.debug('Loading the message and parsing it')
    request = models.incoming.IncomingRequest.parse_obj({"payload": json.loads(message)})
    _executor_logger.debug('Successfully loaded the message. Parsed message content:\n%s',
                           request.json(by_alias=False))
    # Access the payload and check if the type of the payload
    _executor_logger.debug('Checking the type of the request')
    payload_type = type(request.payload)
    _executor_logger.debug('Detected the following request type: %s', payload_type)
    if payload_type == models.incoming.ValidateTokenRequest:
        _executor_logger.info('Running a new token introspection request')
        introspection_result = tools.run_token_introspection(request.payload)
        return introspection_result.json(by_alias=True, exclude_none=True).encode('utf-8')
    elif payload_type == models.incoming.CreateScopeRequest:
        # Create a new database entry
        scope = database.tables.Scope(
            name=request.payload.scope_name,
            description=request.payload.scope_description,
            oauth2_value=request.payload.scope_value
        )
        # Add the object to the database
        _scope = database.crud.add_object_to_database(scope, next(database.session()))
        return models.responses.ScopeAddedResponse.from_orm(_scope).json(by_alias=True).encode(
            'utf-8')
    else:
        return json.dumps({"error": "not_implemented"}).encode('utf-8')
