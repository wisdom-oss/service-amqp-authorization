""""""
import logging

import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm

import settings

__logger = logging.getLogger(__name__)

_settings = settings.DatabaseSettings()
"""The settings for the database connection"""

_engine = sqlalchemy.engine.create_engine(
    url=_settings.dsn,
    pool_recycle=90  # Reconnect to the database every 90 seconds, to keep the connection from
                     # aborting
)

_database_session = sqlalchemy.orm.sessionmaker(_engine)
"""A session maker which will generate active database session"""


def session() -> sqlalchemy.orm.Session:
    """
    Get an opened connection session to the database
    
    :return: A opened connection session
    :rtype: sqlalchemy.orm.Session
    """
    _session: sqlalchemy.orm.Session = _database_session()
    try:
        yield _session
    finally:
        _session.close()
        

def engine() -> sqlalchemy.engine.Engine:
    """
    Get the database engine
    
    :return: The database engine
    :rtype: sqlalchemy.engine.Engine
    """
