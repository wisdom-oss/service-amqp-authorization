"""The module containing functions for the AMQP server"""
import http

import sqlalchemy.exc
import ujson
import logging

import pydantic.error_wrappers

import database.crud
import database.tables
import exceptions
import models.requests
import models.responses
import settings
import tools

_content_validation_logger = logging.getLogger("content_validation")
_executor_logger = logging.getLogger("executor")


def content_validator(message: bytes) -> bool:
    """Check if the content is parseable into the incoming request model"""
    try:
        request = models.requests.IncomingRequest.parse_obj({"payload": ujson.loads(message)})
    except pydantic.ValidationError as e:
        _content_validation_logger.critical("Rejected message", exc_info=e)
        return False
    return True


def executor(message: bytes) -> bytes:
    """Parse the message again and run the appropriate action"""
    try:
        _executor_logger.debug("Loading the message and parsing it")
        request = models.requests.IncomingRequest.parse_obj({"payload": ujson.loads(message)})
        _executor_logger.debug(
            "Successfully loaded the message. Parsed message content:\n%s",
            request.json(by_alias=False),
        )
        # Access the payload and check if the type of the payload
        _executor_logger.debug("Checking the type of the request")
        payload = request.payload
        payload_type = type(payload)
        _executor_logger.debug("Detected the following request type: %s", payload_type)
        if payload_type == models.requests.TokenValidationData:
            _executor_logger.info("Running a new token introspection request")
            introspection_result = tools.run_token_introspection(request.payload)
            return ujson.dumps(
                introspection_result.dict(by_alias=True, exclude_none=True),
                sort_keys=True,
                ensure_ascii=False,
            ).encode("utf-8")
        elif payload_type == models.requests.ScopeCreationData:
            # Create a new database entry
            database.crud.store_new_scope(request.payload)
            scope = database.crud.get_scope(request.payload.scope_string_value)
            if scope is None:
                raise exceptions.ServiceException(
                    error_code="SCOPE_NOT_CREATED",
                    error_name="Scope not created",
                    error_description="The requested scope was not created",
                    status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            else:
                return ujson.dumps(scope.dict()).encode("utf-8")
        elif payload_type == models.requests.ScopeCheckData:
            # Try to get a scope from the database
            scope = database.crud.get_scope(request.payload.scope_identifier)
            if scope is None:
                raise exceptions.ServiceException(
                    error_code="SCOPE_NOT_FOUND",
                    error_name="Scope unavailable",
                    error_description="The requested scope does not exist",
                    status_code=http.HTTPStatus.NOT_FOUND,
                )
            else:
                return ujson.dumps(scope.dict()).encode("utf-8")
        elif payload_type == models.requests.ScopeUpdateData:
            # Try to get a scope from the database
            if request.payload.scope_identifier in ["administrator", "me"]:
                raise exceptions.ServiceException(
                    error_code="SCOPE_NOT_MODIFIABLE",
                    error_name="Scope not modifiable",
                    error_description="The requested scope may not be changed since the scope is a core scope used by "
                    "the authorization service",
                    status_code=http.HTTPStatus.FORBIDDEN,
                )
            scope = database.crud.get_scope(request.payload.scope_identifier)
            if scope is None:
                raise exceptions.ServiceException(
                    error_code="SCOPE_NOT_FOUND",
                    error_name="Scope unavailable",
                    error_description="The requested scope does not exist",
                    status_code=http.HTTPStatus.NOT_FOUND,
                )
            scope.name = scope.name if request.payload.name is None else payload.name
            scope.description = (
                scope.description if payload.description is None else payload.description
            )
            database.crud.store_changed_scope(scope)
            scope = database.crud.get_scope(scope.id)
            return ujson.dumps(scope.dict(by_alias=True)).encode("utf-8")
    except exceptions.ServiceException as exception:
        content = {
            "httpCode": exception.http_code.value,
            "httpError": exception.http_code.phrase,
            "error": settings.ServiceConfiguration().name + f".{exception.error_code}",
            "errorName": exception.error_name,
            "errorDescription": exception.error_description,
        }
        return ujson.dumps(content).encode("utf-8")
    except sqlalchemy.exc.IntegrityError as e:
        content = {
            "httpCode": http.HTTPStatus.CONFLICT.value,
            "httpError": http.HTTPStatus.CONFLICT.phrase,
            "error": settings.ServiceConfiguration().name + f".DUPLICATE_ENTRY",
            "errorName": "Constraint Violation",
            "errorDescription": "The resource you are trying to create already exists",
        }
        return ujson.dumps(content).encode("utf-8")
    except Exception as e:
        print(e)
        content = {
            "httpCode": http.HTTPStatus.INTERNAL_SERVER_ERROR.value,
            "httpError": http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            "error": settings.ServiceConfiguration().name + f".INTERNAL_ERROR",
            "errorName": "Internal Service Error",
            "errorDescription": "The service encountered an internal error: " + str(e),
        }
        return ujson.dumps(content).encode("utf-8")
