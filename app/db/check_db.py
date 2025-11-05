from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_xzR9md7PXfih@ep-sparkling-fire-a1qclnt9-pooler.ap-southeast-1.aws.neon.tech/neondb"
async def check():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            print("✅ Connection successful!")
    except Exception as e:
        print("❌ Connection failed:", e)

asyncio.run(check())