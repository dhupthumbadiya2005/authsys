import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def get_database():
    return db.database

async def connect_to_mongo():
    """Create database connection"""
    mongodb_url = os.getenv("MONGODB_URL")
    
    # Add SSL configuration for MongoDB Atlas - disable SSL verification for development
    db.client = AsyncIOMotorClient(
        mongodb_url,
        tlsCAFile=None,  # Use system CA certificates
        tlsAllowInvalidCertificates=True,  # Allow invalid certificates for development
        tlsAllowInvalidHostnames=True,     # Allow invalid hostnames for development
        retryWrites=True,
        w='majority'
    )
    
    db.database = db.client.authsys
    
    try:
        # Test the connection
        await db.client.admin.command('ping')
        print("Connected to MongoDB")
        
        # Create TTL index for challenges collection (auto-delete expired challenges)
        await db.database.challenges.create_index(
            "expires_at", 
            expireAfterSeconds=0
        )
        print("Created TTL index for challenges")
        
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        # Don't fail startup, just log the error
        pass

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")

# Helper functions for database operations
async def get_user_by_username(username: str):
    """Get user by username"""
    database = await get_database()
    return await database.users.find_one({"username": username})

async def get_user_by_user_id(user_id: str):
    """Get user by WebAuthn user_id"""
    database = await get_database()
    return await database.users.find_one({"user_id": user_id})

async def create_user(user_data: dict):
    """Create a new user"""
    database = await get_database()
    result = await database.users.insert_one(user_data)
    return result.inserted_id

async def update_user_last_login(username: str):
    """Update user's last login timestamp"""
    database = await get_database()
    await database.users.update_one(
        {"username": username},
        {"$set": {"last_login": datetime.utcnow()}}
    )

async def get_credentials_by_user_id(user_id: str):
    """Get all credentials for a user"""
    database = await get_database()
    cursor = database.credentials.find({"user_id": user_id})
    return await cursor.to_list(length=None)

async def create_credential(credential_data: dict):
    """Create a new credential"""
    database = await get_database()
    result = await database.credentials.insert_one(credential_data)
    return result.inserted_id

async def update_credential_sign_count(credential_id: str, sign_count: int):
    """Update credential sign count"""
    database = await get_database()
    await database.credentials.update_one(
        {"credential_id": credential_id},
        {"$set": {"sign_count": sign_count}}
    )

async def create_challenge(challenge_data: dict):
    """Create a new challenge"""
    database = await get_database()
    result = await database.challenges.insert_one(challenge_data)
    return result.inserted_id

async def get_challenge(challenge: str, username: str, challenge_type: str):
    """Get and delete a challenge (single use)"""
    database = await get_database()
    result = await database.challenges.find_one_and_delete({
        "challenge": challenge,
        "username": username,
        "type": challenge_type,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    return result
