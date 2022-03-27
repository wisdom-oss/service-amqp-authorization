"""A module describing the incoming data in pydantic data models"""
import typing

import pydantic

import models
import enums


class ValidateTokenRequest(models.BaseModel):
    """A request for validating the sent token against the sent scope"""
    
    action: typing.Literal[enums.Action.CHECK_TOKEN_SCOPE]
    
    oauth2_token: str = pydantic.Field(
        default=...,
        alias='token',
        title='OAuth2.0 Access Token',
        description='The token which shall be checked against the sent scope'
    )
    """
    OAuth2.0 Access Token
    
    The token which shall be checked against the sent scope
    """
    
    oauth2_scope: str = pydantic.Field(
        default=...,
        alias='scope',
        title='OAuth2.0 Scope',
        description='The scope which shall be used for checking the token'
    )
    """
    OAuth2.0 Scope
    
    The value of the scope which needs to be in the token's scopes list for the check to be
    successful
    """
    

class CreateScopeRequest(models.BaseModel):
    """"""
    
    action: typing.Literal[enums.Action.ADD_SCOPE]

    scope_name: str = pydantic.Field(
        default=...,
        title='Name',
        description='The name of the scope given by the creator',
        alias='name'
    )
    """Name of the scope"""

    scope_description: str = pydantic.Field(
        default='',
        title='Description',
        description='Textual description of the scope. This may contain hint as to what this '
                    'scope may be used for',
        alias='description'
    )
    """Textual description of the scope"""

    scope_value: str = pydantic.Field(
        default=...,
        title='Value',
        description='The value represents the scope in a OAuth2 scope string',
        alias='value'
    )
    """OAuth2 scope string value identifying the scope"""


class IncomingRequest(models.BaseModel):
    """A model for incoming requests"""
    
    payload: typing.Union[ValidateTokenRequest, CreateScopeRequest] = pydantic.Field(
        default=..., discriminator='action'
    )
