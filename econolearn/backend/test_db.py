from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Successfully connected to the database!")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
