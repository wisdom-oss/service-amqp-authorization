import typing
import pydantic

import enums
import models
from models import BaseModel as __BaseModel


class TokenValidationData(__BaseModel):
    action: typing.Literal[enums.Action.CHECK_TOKEN_SCOPE]

    token: str = pydantic.Field(default=...)
    """The token that shall be validated"""

    scopes: typing.Optional[typing.Union[list[str], str, None]] = pydantic.Field(default=None)
    """The scopes which the token needs to pass the validation"""

    @pydantic.validator("scopes")
    def convert_scope_string_to_list(cls, v):
        if type(v) is list:
            return v
        elif type(v) is str:
            return v.split()
        elif v is None:
            return v
        else:
            raise TypeError("The scope parameter only accepts lists or strings")


class ScopeCheckData(__BaseModel):
    action: typing.Literal[enums.Action.CHECK_SCOPE]

    scope_identifier: typing.Union[str, int] = pydantic.Field(default=...)


class ScopeUpdateData(__BaseModel):
    action: typing.Literal[enums.Action.EDIT_SCOPE]

    name: typing.Optional[str] = pydantic.Field(default=...)
    """The name of the scope"""

    description: typing.Optional[str] = pydantic.Field(default=...)
    """The description of the scope"""


class ScopeCreationData(__BaseModel):
    action: typing.Literal[enums.Action.ADD_SCOPE]

    name: str = pydantic.Field(default=...)
    """The name of the scope"""

    description: str = pydantic.Field(default=...)
    """The description of the scope"""

    scope_string_value: str = pydantic.Field(default=...)
    """The value by which the scope is identifiable in a scope string"""


class IncomingRequest(__BaseModel):
    payload: typing.Union[TokenValidationData, ScopeCreationData, ScopeUpdateData, ScopeCheckData]
