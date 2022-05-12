import datetime
import typing

import pydantic

import models


class UserAccount(models.BaseModel):

    id: int = pydantic.Field(default=..., title="Internal Account ID")
    """Internal Account ID"""

    first_name: str = pydantic.Field(default=..., title="First Name")
    """The first name of the user who is the owner of the account"""

    last_name: str = pydantic.Field(default=..., title="Last Name")
    """The last name of the user who is the owner of the account"""

    username: str = pydantic.Field(default=..., title="Username")
    """The username of the account"""

    password: pydantic.SecretStr = pydantic.Field(default=..., title="Password")
    """The password of the account"""

    active: bool = pydantic.Field(default=..., title="Active Account")
    """Indicator if the account is active"""


class Scope(models.BaseModel):

    id: int = pydantic.Field(default=None)
    """The internal database id of the scope"""

    name: str = pydantic.Field(default=...)
    """The name of the scope"""

    description: str = pydantic.Field(default=...)
    """The description of the scope"""

    scope_string_value: str = pydantic.Field(default=...)
    """The value by which the scope is identifiable in a scope string"""


class TokenInformation(models.BaseModel):

    id: int = pydantic.Field(default=None)
    """The internal database id of the token"""

    value: pydantic.SecretStr = pydantic.Field(default=...)
    """The encoded value of the token"""

    active: bool = pydantic.Field(default=...)
    """The status of the token"""

    expires: datetime.datetime = pydantic.Field(default=...)
    """The time and date of expiration"""

    created: typing.Optional[datetime.datetime] = pydantic.Field(default=None)
    """The time and date on which the token has been created"""

    owner_id: int = pydantic.Field(default=...)
    """The id of the account this token is associated to"""
