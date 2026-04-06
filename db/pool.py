import os

import asyncpg

pool: asyncpg.Pool | None = None

async def init_db() -> None:
    global pool
    pool = await asyncpg.create_pool(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 5432)),
        min_size=1,
        max_size=10,
    )
    await init_tables(pool)

async def init_tables(p: asyncpg.Pool) -> None:
    async with p.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         BIGSERIAL PRIMARY KEY,
                peer_id    BIGINT UNIQUE NOT NULL,
                username   TEXT,
                first_name TEXT,
                last_name  TEXT
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id      BIGSERIAL PRIMARY KEY,
                peer_id BIGINT UNIQUE NOT NULL
            );
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id         BIGSERIAL PRIMARY KEY,
                chat_id    BIGINT REFERENCES chats(id),
                user_id    BIGINT REFERENCES users(id),
                text       TEXT,
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
        """)

async def close_db() -> None:
    await pool.close()