import enum


class Action(str, enum.Enum):
    """The actions which are available for this service"""
    
    CHECK_TOKEN_SCOPE = "validate_token"
    """Check the scope of a token and return if the token is valid and has the scope"""
    
    ADD_SCOPE = "add_scope"
    """Add a scope to the authorization system"""
    
    EDIT_SCOPE = "edit_scope"
    """Edit a scope already in the authorization system"""
    
    DELETE_SCOPE = "delete_scope"
    """Remove a scope from the authorization system"""
    
    CHECK_SCOPE = "check_scope"
    """Check if a scope is already present in the system"""
    

class TokenType(str, enum.Enum):
    """The different tokens which are available for introspection"""
    
    ACCESS_TOKEN = "access_token"
    """A OAuth2.0 Access Token"""
    
    REFRESH_TOKEN = "refresh_token"
    """A OAuth2.0 Refresh Token"""


class TokenIntrospectionFailure(str, enum.Enum):
    """
    The reasons why a token introspection has failed and did not return that the token is valid
    """
    
    TOKEN_MALFORMED = "token_format_error"
    """The token was not formatted correctly to be introspected"""
    
    NO_TOKEN_FOUND = "no_token_found"
    """No token with this value has been found in the database"""
    
    TOKEN_EXPIRED = "token_expired"
    """The token was found in the database but is expired"""
    
    TOKEN_USED_BEFORE_CREATION = "token_not_alive"
    """The token has been used before it's creation time"""
    
    INSUFFICIENT_SCOPE = "insufficient_scope"
    """The token is not allowed to use this scope"""
