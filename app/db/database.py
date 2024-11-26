from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# MongoDB connection string
MONGO_DETAILS = config(
    "MONGO_DETAILS", default="mongodb://root:example@localhost:27017"
)
DATABASE_NAME = config("DATABASE_NAME", default="devtodo")

# Instantiate a client
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client[DATABASE_NAME]
