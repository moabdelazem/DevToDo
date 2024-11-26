from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import uuid4, UUID


class Todo(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")  # Use uuid4 as default
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, min_length=1, max_length=100)
    completed: bool = Field(default=False)

    # Update the Config class to ConfigDict
    model_config = ConfigDict(
        populate_by_name=True,  # Replaces 'allow_population_by_field_name'
        json_schema_extra={
            "example": {
                "_id": "123e4567-e89b-12d3-a456-426614174000",  # Example UUID
                "title": "Do Homework",
                "description": "Complete all assigned homework.",
                "completed": False,
            }
        },
    )

    # If needed, implement custom serialization for UUID (instead of json_encoders)
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Ensure UUID is serialized as a string in the output
        if "id" in data:
            data["id"] = str(data["id"])  # Serialize UUID as string
        return data
