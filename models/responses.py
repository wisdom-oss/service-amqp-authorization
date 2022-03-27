"""Data models for outgoing communication"""
import typing

import pydantic

import enums
import models.incoming


class TokenIntrospectionResult(models.BaseModel):
    """The result of an introspection request for an access token"""
    
    is_active: bool = pydantic.Field(
        default=False,
        alias='active'
    )
    """
    Token Status **[required]**
    
    If the value is ``True`` the token is valid for the scope(s) at the current time
    """
    
    scopes: typing.Optional[list[str]] = pydantic.Field(
        default=None,
        alias='scope'
    )
    """
    Token Scopes *[optional]*
    
    A :class:`list` containing the OAuth2.0 Scopes the token was assigned. If the request contained
    a scope this list will only contain the scope which was sent in the request.
    """
    
    username: typing.Optional[str] = pydantic.Field(
        default=None,
        alias='username'
    )
    """
    Account Username *[optional]*
    
    This attribute contains the username associated to the introspected token
    """
    
    token_type: typing.Optional[enums.TokenType] = pydantic.Field(
        default=None,
        alias='token_type'
    )
    """
    Token Type *[optional]*
    
    The type of token which has been sent to the service for an introspection.
    Available values are:
      * ``access_token``
      * ``refresh_token``q
    """
    
    expires_at: typing.Optional[int] = pydantic.Field(
        default=None,
        alias='exp'
    )
    """
    Expiry Time and Date
    
    This attribute contains the time at which the token will expire as a UNIX timestamp
    """
    
    created_at: typing.Optional[str] = pydantic.Field(
        default=None,
        alias='iat'
    )
    """
    Creation Time and Date
    
    This attribute contains the time at which the token was created as a UNIX timestamp
    """
    
    error_reason: typing.Optional[enums.TokenIntrospectionFailure] = pydantic.Field(
        default=None,
        alias='reason'
    )
    """
    Introspection Failure Reason
    
    The reason why the token introspection has failed
    """


class ScopeAddedResponse(models.incoming.CreateScopeRequest):
    
    id: int = pydantic.Field(
        default=...,
        alias='scope_id'
    )
    """The internal ID of the scope"""
    
    class Config:
        orm_mode = True
