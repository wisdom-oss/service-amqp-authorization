"""Utilities for creating reading updating and deleting data"""

import typing

import sqlalchemy.orm

import database.tables

DatabaseObject = typing.TypeVar(
    'DatabaseObject',
    database.tables.Scope, database.tables.TokenScopes, database.tables.AccessToken
)


def _add_object_to_database(obj: DatabaseObject, session: sqlalchemy.orm.Session) -> DatabaseObject:
    """
    Add the specified object to the database
    
    :param obj: The object which shall be inserted into the database
    :type obj: DatabaseObject
    :param session: The session used to add the object to the database
    :type session: sqlalchemy.orm.Session
    :return: The inserted object, after it has been refreshed
    :rtype: DatabaseObject
    """
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def get_access_token(token: str, session: sqlalchemy.orm.Session) -> database.tables.AccessToken:
    """
    Get the database entry of the specified token
    
    :param token: The token value
    :type token: str
    :param session: The opened database session
    :type session: sqlalchemy.orm.Session
    :return: The database entry which has been found
    :rtype: tables.AccessToken
    :raises ValueError: The specified token could not be found
    """
    _db_token = session.query(
        database.tables.AccessToken).filter(database.tables.AccessToken.value == token).first()
    if _db_token is None:
        raise ValueError('The token was not found in the database')
    return _db_token
