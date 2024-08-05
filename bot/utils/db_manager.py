import os

import aiosqlite

DB_PATH = f"{os.path.dirname(__file__)}/../data/database.db"


async def add_death(user_id: int, death_id: str, points: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT count FROM deaths WHERE user_id = ? AND death_id = ?",
            (user_id, death_id),
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                new_count = row[0] + 1
                await db.execute(
                    "UPDATE deaths SET count = ? WHERE user_id = ? AND death_id = ?",
                    (new_count, user_id, death_id),
                )
            else:
                await db.execute(
                    "INSERT INTO deaths (user_id, death_id, count) VALUES (?, ?, ?)",
                    (user_id, death_id, 1),
                )

        await db.execute(
            "UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id)
        )
        await db.commit()


async def get_user_deaths(user_id: int) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT death_id, count FROM deaths WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchall()
