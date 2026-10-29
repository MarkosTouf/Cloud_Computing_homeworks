from pydantic import BaseModel, ConfigDict, Field


# Data accepted when creating a course.
# This schema describes the request body for POST /courses.
class BookCreate(BaseModel):
    # Field adds validation rules before the route function runs.
    title: str = Field(min_length=2)
    author: str = Field(min_length=2)
    year: int = Field(gt=1900)


# Data returned by the API.
# This schema describes the response shape sent back to the client.
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int

    # This allows Pydantic to read values from SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)