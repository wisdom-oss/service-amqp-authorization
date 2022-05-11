"""Module containing all settings which are used in the application"""
import typing

import pydantic
from pydantic import BaseSettings, AmqpDsn, stricturl, Field


class ServiceSettings(BaseSettings):
    """Settings related to the general service execution"""

    name: str = Field(
        default="authorization-service",
        title="Service Name",
        description="The name of the service which is used for registering at the service "
                    "registry and for identifying this service in amqp responses",
        env="CONFIG_SERVICE_NAME",
    )
    """
    Application Name
    
    The name of the service which is used for registering at the service registry and for
    identifying this service in amqp responses
    """

    log_level: str = Field(
        default="INFO",
        title="Logging Level",
        description="The level of logging which the root logger will use",
        env="CONFIG_LOGGING_LEVEL",
    )
    """
    Logging Level
    
    The level of logging which will be used by the root logger
    """

    class Config:
        """Configuration of the service settings"""

        env_file = ".env"
        """Allow loading the values for the service settings from the specified file"""


class AMQPConfiguration(pydantic.BaseSettings):
    dsn: pydantic.AmqpDsn = pydantic.Field(
        default=...,
        title="AMQP Data Source Name",
        description="The data source name pointing to an installation of a RabbitMQ message broker",
        env="CONFIG_AMQP_DSN",
        alias="CONFIG_AMQP_DSN",
    )
    """
    AMQP Data Source Name

    The data source name pointing to an installation of the RabbitMQ message broker
    """

    exchange: typing.Optional[str] = pydantic.Field(
        default="authorization-service",
        title="AMQP Send Exchange",
        description="The exchange to which this service will send messages",
        env="CONFIG_AMQP_EXCHANGE",
        alias="CONFIG_AMQP_BIND_EXCHANGE",
    )
    """
    AMQP Send Exchange

    The exchange to which this service will send the messages
    """

    class Config:
        """Configuration of the AMQP related settings"""

        env_file = ".env"
        """The file from which the settings may be read"""


class DatabaseSettings(BaseSettings):
    """Settings related to the connections to the geo-data server"""

    dsn: pydantic.PostgresDsn = Field(
        default=...,
        title="PostgreSQL Database Service Name",
        description="A uri pointing to the mariadb containing the data for this service",
        env="CONFIG_DB_DSN",
    )
    """
    PostgreSQL Database Service Name

    An URI pointing to the installation of a PostgreSQL database which has the data required for
    this service
    """

    class Config:
        """Configuration of the AMQP related settings"""

        env_file = ".env"
        """The file from which the settings may be read"""
