from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4, UUID


class Todo(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")  # Use uuid4 as default
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1, max_length=100)
    completed: bool = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {UUID: str}  # Ensure UUID is serialized as a string
        schema_extra = {
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",  # Example UUID
                "title": "Do Homework",
                "description": "Complete all assigned homework.",
                "completed": False,
            }
        }
