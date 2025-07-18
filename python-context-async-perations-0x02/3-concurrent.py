import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    users_all, users_old = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users_all)
    print("Users older than 40:", users_old)

# ✅ Run concurrent queries
asyncio.run(fetch_concurrently())
