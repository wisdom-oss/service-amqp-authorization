"""The module containing functions for the AMQP server"""
import pydantic.error_wrappers

import database.crud
import models.incoming


def content_validator(message: bytes) -> bool:
    """Check if the content is parseable into the incoming request model"""
    try:
        models.incoming.IncomingRequest.parse_raw(message)
        return True
    except pydantic.error_wrappers.ValidationError:
        return False
    

def executor(message: bytes) -> bytes:
    """Parse the message again and run the appropriate action"""
    request = models.incoming.IncomingRequest.parse_raw(message)
    # Access the payload and check if the type of the payload
    payload_type = type(request.payload)
    if payload_type == models.incoming.ValidateTokenRequest:
        session = next(database.session())
        try:
            _token = database.crud.get_access_token(request.payload.oauth2_token, session)
        except ValueError:
            pass
