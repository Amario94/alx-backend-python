import asyncio
import aiosqlite

DB_NAME = "users.db"

# 🔹 Asynchronous function to fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All users:")
            for row in rows:
                print(row)
            return rows

# 🔹 Asynchronous function to fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers older than 40:")
            for row in rows:
                print(row)
            return rows

# 🔹 Run both queries concurrently
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

# 🔹 Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
