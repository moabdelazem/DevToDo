from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection string
MONGO_DETAILS = "mongodb://localhost:27017"
DATABASE_NAME = "devtodo"

# Instantiate a client
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client[DATABASE_NAME]
