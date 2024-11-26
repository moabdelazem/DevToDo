from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class Todo(BaseModel):
    id: UUID = Field(default_factory=UUID, alias="_id")
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(min_length=1, max_length=100)
    compelted: bool = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Do Homework",
                "description": "Do all the homework",
                "completed": False,
            }
        }
