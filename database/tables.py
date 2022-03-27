"""Object Relational Mapping classes and objects"""
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()
"""The base class for all ORM classes"""

FOREIGN_KEY_OPTIONS = {
    "onupdate": "CASCASE",
    "ondelete": "CASCADE"
}
"""Default options for all foreign key relationships"""


class Scope(Base):
    """A scope present in the database"""
    
    __tablename__ = "scopes"
    """The name of the database"""
    
    id = sqlalchemy.Column(
        name='scope_id',
        type=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    """The internal id of the scope"""
    
    name = sqlalchemy.Column(
        name='scope_name',
        type=sqlalchemy.String(length=255),
        unique=True
    )
    """The name of the scope"""
    
    description = sqlalchemy.Column(
        name='scope_description',
        type=sqlalchemy.Text
    )
    """The textual description of the scope"""
    
    oauth2_value = sqlalchemy.Column(
        name='scope_value',
        type=sqlalchemy.String(length=255),
        unique=True
    )
    """The string identifying the scope in a OAuth2 scope string"""
    
    
class AccessToken(Base):
    """An access token which has been issued to a user"""
    
    __tablename__ = "access_tokens"
    """The name of the database"""
    
    id = sqlalchemy.Column(
        name='token_id',
        type=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    """The internal id of the access token"""
    
    value = sqlalchemy.Column(
        name='token',
        type=sqlalchemy.String(length=36),
        unique=True
    )
    """The token which has been issued to the user"""
    
    is_active = sqlalchemy.Column(
        name='active',
        type=sqlalchemy.Boolean,
        default=True
    )
    """The status of the token"""
    
    expires_at = sqlalchemy.Column(
        name='expires',
        type=sqlalchemy.Integer,
        nullable=False
    )
    """The UNIX timestamp indicating the expiration time and date of the token"""
    
    created_at = sqlalchemy.Column(
        name='created',
        type=sqlalchemy.Integer,
        nullable=False
    )
    """The UNIX timestamp indicating the creation time and date of the token"""
    
    scopes = sqlalchemy.orm.relationship("Scope", secondary='token_scopes')
    """The scopes assigned to the token during the creation"""
    

class TokenScopes(Base):
    """The mapping table which assigns the scopes to the access tokens"""
    
    __tablename__ = "token_scopes"
    """The name of the mapping table"""
    
    mapping_id = sqlalchemy.Column(
        type=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    """The internal id of the mapping"""
    
    token_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey('access_tokens.token_id', **FOREIGN_KEY_OPTIONS),
        type=sqlalchemy.Integer
    )
    """The id of the token which is the associated to the scope"""
    
    scope_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey('scopes.scope_id', **FOREIGN_KEY_OPTIONS),
        type=sqlalchemy.Integer
    )
    """The id of the scope which is associated to the token"""
