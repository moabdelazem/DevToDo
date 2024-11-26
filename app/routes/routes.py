from fastapi import APIRouter, HTTPException
from uuid import UUID
from bson import Binary
from model.model import Todo
from db.database import db

router = APIRouter()


# Convert UUID to BSON Binary format
def uuid_to_binary(uuid: UUID) -> Binary:
    return Binary.from_uuid(uuid)


# Convert BSON Binary back to UUID
def binary_to_uuid(binary: Binary) -> UUID:
    return binary.as_uuid()


@router.get("/todos", response_model=list[Todo])
async def list_todos():
    todos = await db.todo.find().to_list(1000)
    # Convert MongoDB ObjectId `_id` to UUID if needed
    for todo in todos:
        todo["_id"] = binary_to_uuid(todo["_id"])  # Convert BSON Binary to UUID
    return todos


@router.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    print(f"Received Todo: {todo}")  # Debugging
    # Convert UUID to BSON Binary before inserting into the database
    todo_dict = todo.dict(by_alias=True)
    todo_dict["_id"] = uuid_to_binary(todo.id)  # Convert UUID to BSON Binary

    new_todo = await db.todo.insert_one(todo_dict)
    created_todo = await db.todo.find_one({"_id": new_todo.inserted_id})

    if created_todo is None:
        raise HTTPException(status_code=500, detail="Todo not created")

    created_todo["_id"] = binary_to_uuid(
        created_todo["_id"]
    )  # Convert BSON Binary to UUID
    return created_todo


@router.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: UUID):
    todo = await db.todo.find_one({"_id": uuid_to_binary(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo["_id"] = binary_to_uuid(todo["_id"])
    return todo


@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: UUID, todo: Todo):
    todo_dict = todo.dict(by_alias=True)
    todo_dict["_id"] = uuid_to_binary(todo_id)
    updated_todo = await db.todo.find_one_and_update(
        {"_id": uuid_to_binary(todo_id)},
        {"$set": todo_dict},
        return_document=True,
    )
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo["_id"] = binary_to_uuid(updated_todo["_id"])
    return updated_todo


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: UUID):
    todo = await db.todo.find_one_and_delete({"_id": uuid_to_binary(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo["_id"] = binary_to_uuid(todo["_id"])
    return todo


@router.put("/todos/{todo_id}/complete", response_model=Todo)
async def complete_todo(todo_id: UUID):
    updated_todo = await db.todo.find_one_and_update(
        {"_id": uuid_to_binary(todo_id)},
        {"$set": {"completed": True}},
        return_document=True,
    )
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    updated_todo["_id"] = binary_to_uuid(updated_todo["_id"])
    return updated_todo
