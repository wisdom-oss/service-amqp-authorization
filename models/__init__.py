"""A module containing the data models which will be used for a data validation"""
import pydantic


class BaseModel(pydantic.BaseModel):
    """A modified base model which allows the usage for inheriting configurations"""
    
    class Config:
        """The configuration for the modified base model"""
        
        arbitrary_types_allowed = True
        """Allow arbitrary types for type hints"""
        
        allow_population_by_field_name = True
        """Allow the population of the fields by their name"""
