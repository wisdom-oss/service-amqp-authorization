""""""
import logging

import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.orm

import settings

__logger = logging.getLogger(__name__)

_settings = settings.DatabaseConfiguration()
"""The settings for the database connection"""

engine = sqlalchemy.engine.create_engine(
    url=_settings.dsn,
    pool_recycle=90  # Reconnect to the database every 90 seconds, to keep the connection from
    # aborting
)
