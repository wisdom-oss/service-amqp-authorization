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
        sqlalchemy.Integer,
        name='scope_id',
        primary_key=True,
        autoincrement=True
    )
    """The internal id of the scope"""
    
    name = sqlalchemy.Column(
        sqlalchemy.String(length=255),
        name='scope_name',
        unique=True
    )
    """The name of the scope"""
    
    description = sqlalchemy.Column(
        sqlalchemy.Text,
        name='scope_description'
    )
    """The textual description of the scope"""
    
    oauth2_value = sqlalchemy.Column(
        sqlalchemy.String(length=255),
        name='scope_value',
        unique=True
    )
    """The string identifying the scope in a OAuth2 scope string"""
    
    
class AccessToken(Base):
    """An access token which has been issued to a user"""
    
    __tablename__ = "access_tokens"
    """The name of the database"""
    
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        name='token_id',
        primary_key=True,
        autoincrement=True
    )
    """The internal id of the access token"""
    
    value = sqlalchemy.Column(
        sqlalchemy.String(length=36),
        name='token',
        unique=True
    )
    """The token which has been issued to the user"""
    
    is_active = sqlalchemy.Column(
        sqlalchemy.Boolean,
        name='active',
        default=True
    )
    """The status of the token"""
    
    expires_at = sqlalchemy.Column(
        sqlalchemy.Integer,
        name='expires',
        nullable=False
    )
    """The UNIX timestamp indicating the expiration time and date of the token"""
    
    created_at = sqlalchemy.Column(
        sqlalchemy.Integer,
        name='created',
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
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    """The internal id of the mapping"""
    
    token_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('access_tokens.token_id', **FOREIGN_KEY_OPTIONS),
    )
    """The id of the token which is the associated to the scope"""
    
    scope_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('scopes.scope_id', **FOREIGN_KEY_OPTIONS),
    )
    """The id of the scope which is associated to the token"""
