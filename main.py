from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

MONGO_URI = os.getenv("MONGO_URI") # Access the MongoDB URI from environment variables
client = AsyncIOMotorClient(MONGO_URI) # Initialize the MongoDB client
db = client["GenAI"] # Access the database
gen_data = db["coll1"]

app = FastAPI()

class my_data(BaseModel):   # Define a Pydantic model for the data to be inserted
    name : str
    phone : int
    age : int


@app.post("/data/insert")
async def data_insert(data : my_data):  #
    result = await gen_data.insert_one(data.dict()) # Insert one data into the collection
    return str(result.inserted_id) # Return the ID of the inserted document

#async -> This keyword is used to define an asynchronous function. It allows the function to run without blocking the main thread, enabling other operations to continue while waiting for the completion of the asynchronous task. In this context, it allows the FastAPI application to handle multiple requests concurrently without waiting for the database operation to complete.

#await -> This keyword is used to pause the execution of an asynchronous function until the awaited task is completed. In this context, it is used to wait for the result of the insert_one operation on the MongoDB collection before proceeding to return the inserted ID.


def helper(doc):
    doc["id"] = str(doc["_id"]) # Convert the ObjectId to a string and assign it to the "id" field
    del doc["_id"] # Remove the original "_id" field from the document
    return doc


@app.get("/data/get")
async def get_data():
    items = []
    cursor = gen_data.find({})
    async for document in cursor:
        items.append(helper(document))
    return items