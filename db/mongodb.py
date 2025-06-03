from pymongo import AsyncMongoClient
from config import settings
from fastapi import FastAPI

class MongoDB:
    client: AsyncMongoClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    try:
        # print(settings.MONGODB_URL)
        uri=settings.MONGODB_URL
        mongodb.client = AsyncMongoClient(uri)
        # print("✅ Available databases:", await mongodb.client.list_database_names())
        mongodb.db = mongodb.client.get_database("Strokesence")
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print("❌ MongoDB connection failed:", str(e))
        raise e

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("🛑 MongoDB connection closed")
