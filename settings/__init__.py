"""Settings for the service"""
import pika.exchange_type
import pydantic


class AMQPSettings(pydantic.BaseSettings):
    """Settings related to the connection to a AMQPv0-9-1 compatible message broker"""
    
    dsn: pydantic.AmqpDsn = pydantic.Field(
        default=...,
        alias='dataSourceName',
        title='Data Source Name',
        description='A data source name pointing to a message broker supporting the AMQPv0-9-1 '
                    'protocol',
        env='AMQP_DSN'
    )
    """
    Data Source Name
    
    A URI pointing to a message broker. The message broker needs to implement the version 0-9-1
    of the Advanced Message Queuing Protocol.
    """
    
    exchange_name: str = pydantic.Field(
        default=...,
        alias='exchangeName',
        title='Message Broker Exchange Name',
        description='The name of the exchange the service will bind itself to for receiving '
                    'messages',
        env='AMQP_EXCHANGE_NAME'
    )
    """
    Exchange Name
    
    The name of the exchange this service will bind. The bound exchange will be used to consume
    messages from other microservices
    """
    
    exchange_type: pika.exchange_type.ExchangeType = pydantic.Field(
        default=pika.exchange_type.ExchangeType.fanout,
        alias='exchangeType',
        title='Exchange Type',
        description='The type of the specified exchange'
    )
    """
    Exchange Type
    
    The type of exchange this service will bind itself to.
    
    **Important:** If the exchange already exists the supplied exchange type needs to match the
    one with which the exchange has been created.
    
    Available values:
       * direct
       * fanout (default)
       * headers
       * topic
    """
