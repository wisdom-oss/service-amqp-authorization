import hashlib
import typing

import sqlalchemy.sql

import database
import database.tables
import models.common
import models.requests
import models.responses


# %% Operations for getting users
def get_user_account(identifier: typing.Union[str, int]):
    """
    Get the user account specified in the database

    :param identifier:
    :type identifier:
    :return:
    :rtype:
    """
    if type(identifier) is str:
        user_query = sqlalchemy.sql.select(
            [database.tables.accounts],
            database.tables.accounts.c.username == identifier,
        )
    elif type(identifier) is int:
        user_query = sqlalchemy.sql.select(
            [database.tables.accounts],
            database.tables.accounts.c.id == identifier,
        )
    else:
        raise TypeError("Expected identifier to by either string or int")
    user_query_result = database.engine.execute(user_query).first()
    if user_query_result is None:
        return user_query_result
    return models.common.UserAccount(
        id=user_query_result[0],
        first_name=user_query_result[1],
        last_name=user_query_result[2],
        username=user_query_result[3],
        password=user_query_result[4],
        active=user_query_result[5],
    )


# %% Operations for the scopes
def get_scope(identifier: typing.Union[str, int]):
    if type(identifier) is str:
        scope_query = sqlalchemy.sql.select(
            [database.tables.scopes],
            database.tables.scopes.c.value == identifier,
        )
    elif type(identifier) is int:
        scope_query = sqlalchemy.sql.select(
            [database.tables.scopes],
            database.tables.scopes.c.id == identifier,
        )
    else:
        raise TypeError("Expected identifier to by either string or int")
    scope_query_result = database.engine.execute(scope_query).first()
    if scope_query_result is None:
        return None
    return models.common.Scope(
        id=scope_query_result[0],
        name=scope_query_result[1],
        description=scope_query_result[2],
        scope_string_value=scope_query_result[3],
    )


def get_user_scopes(user: models.common.UserAccount) -> list[models.common.Scope]:
    scope_id_query = sqlalchemy.sql.select(
        [database.tables.account_scopes.c.scopeID],
        database.tables.account_scopes.c.accountID == user.id,
    )
    scope_id_query_result = database.engine.execute(scope_id_query).all()
    scope_ids = [result[0] for result in scope_id_query_result]
    return [get_scope(scope_id) for scope_id in scope_ids]


def get_access_token_scopes(token: models.common.TokenInformation) -> list[models.common.Scope]:
    scope_id_query = sqlalchemy.sql.select(
        [database.tables.access_token_scopes.c.scopeID],
        database.tables.access_token_scopes.c.tokenID == token.id,
    )
    scope_id_query_result = database.engine.execute(scope_id_query).all()
    scope_ids = [result[0] for result in scope_id_query_result]
    return [get_scope(scope_id) for scope_id in scope_ids]


def get_refresh_token_scopes(token: models.common.TokenInformation) -> list[models.common.Scope]:
    scope_id_query = sqlalchemy.sql.select(
        [database.tables.refresh_token_scopes.c.scopeID],
        database.tables.refresh_token_scopes.c.tokenID == token.id,
    )
    scope_id_query_result = database.engine.execute(scope_id_query).all()
    scope_ids = [result[0] for result in scope_id_query_result]
    return [get_scope(scope_id) for scope_id in scope_ids]


def store_changed_scope(scope: models.common.Scope):
    update_scope_query = (
        sqlalchemy.sql.update(database.tables.scopes)
        .where(database.tables.scopes.c.id == scope.id)
        .values(name=scope.name, description=scope.description)
    )
    database.engine.execute(update_scope_query)


def delete_scope(scope: models.common.Scope):
    update_scope_query = sqlalchemy.sql.delete(database.tables.scopes).where(
        database.tables.scopes.c.id == scope.id
    )
    database.engine.execute(update_scope_query)


def store_new_scope(scope_data: models.requests.ScopeCreationData):
    scope_insert_query = sqlalchemy.sql.insert(database.tables.scopes).values(
        name=scope_data.name,
        description=scope_data.description,
        value=scope_data.scope_string_value,
    )
    database.engine.execute(scope_insert_query)


# %% Operations for manipulating access tokens
def get_access_token_data(identifier: typing.Union[str, int]):
    if type(identifier) is str:
        access_token_query = sqlalchemy.sql.select(
            [database.tables.access_token],
            database.tables.access_token.c.value
            == hashlib.sha3_224(identifier.encode("utf-8")).hexdigest(),
        )
    elif type(identifier) is int:
        access_token_query = sqlalchemy.sql.select(
            [database.tables.access_token],
            database.tables.access_token.c.id == identifier,
        )
    else:
        raise TypeError("Expected identifier to by either string or int")
    access_token_query_result = database.engine.execute(access_token_query).first()
    if access_token_query_result is None:
        return None
    return models.common.TokenInformation(
        id=access_token_query_result[0],
        value=access_token_query_result[1],
        active=access_token_query_result[2],
        expires=access_token_query_result[3],
        created=access_token_query_result[4],
        owner_id=access_token_query_result[5],
    )


def get_refresh_token_data(identifier: typing.Union[str, int]):
    if type(identifier) is str:
        access_token_query = sqlalchemy.sql.select(
            [database.tables.refresh_token],
            database.tables.refresh_token.c.value
            == hashlib.sha3_224(identifier.encode("utf-8")).hexdigest(),
        )
    elif type(identifier) is int:
        access_token_query = sqlalchemy.sql.select(
            [database.tables.refresh_token],
            database.tables.refresh_token.c.id == identifier,
        )
    else:
        raise TypeError("Expected identifier to by either string or int")
    access_token_query_result = database.engine.execute(access_token_query).first()
    if access_token_query_result is None:
        return None
    return models.common.TokenInformation(
        id=access_token_query_result[0],
        value=access_token_query_result[1],
        active=access_token_query_result[2],
        expires=access_token_query_result[3],
        owner_id=access_token_query_result[4],
    )


def delete_access_token(token: models.common.TokenInformation):
    delete_access_token_query = sqlalchemy.sql.delete(database.tables.access_token).where(
        database.tables.access_token.c.id == token.id,
    )
    database.engine.execute(delete_access_token_query)


def delete_refresh_token(token: models.common.TokenInformation):
    delete_refresh_token_query = sqlalchemy.sql.delete(database.tables.refresh_token).where(
        database.tables.refresh_token.c.id == token.id
    )
    database.engine.execute(delete_refresh_token_query)


def delete_all_access_tokens(user: models.common.UserAccount):
    delete_access_token_query = sqlalchemy.sql.delete(database.tables.access_token).where(
        database.tables.access_token.c.accountID == user.id,
    )
    database.engine.execute(delete_access_token_query)


def delete_all_refresh_tokens(user: models.common.UserAccount):
    delete_refresh_token_query = sqlalchemy.sql.delete(database.tables.refresh_token).where(
        database.tables.refresh_token.c.accountID == user.id,
    )
    database.engine.execute(delete_refresh_token_query)
