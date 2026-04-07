from typing import List

from db.models import MessageModel, UserModel
import db.pool


async def add_chat(peer_id: int) -> int:
    async with db.pool.pool.acquire() as conn:
        return await conn.fetchval("""
                                   INSERT INTO chats(peer_id)
                                   VALUES ($1)
                                   ON CONFLICT (peer_id) DO UPDATE
                                       SET peer_id = EXCLUDED.peer_id
                                   RETURNING id;
                                   """, peer_id)


async def get_user(peer_id: int) -> UserModel | None:
    async with db.pool.pool.acquire() as conn:
        record = await conn.fetchrow("""
                                     SELECT id, peer_id, username, first_name, last_name
                                     FROM users
                                     WHERE peer_id = $1;
                                     """, peer_id)

        return UserModel(**dict(record)) if record else None


async def add_user(peer_id: int, username: str | None = None,
                   first_name: str | None = None,
                   last_name: str | None = None) -> int:
    async with db.pool.pool.acquire() as conn:
        return await conn.fetchval("""
                                   INSERT INTO users(peer_id, username, first_name, last_name)
                                   VALUES ($1, $2, $3, $4)
                                   ON CONFLICT (peer_id) DO UPDATE
                                       SET username   = EXCLUDED.username,
                                           first_name = EXCLUDED.first_name,
                                           last_name  = EXCLUDED.last_name
                                   RETURNING id;
                                   """, peer_id, username, first_name, last_name)


async def add_message(chat_id: int, user_id: int, text: str) -> int:
    async with db.pool.pool.acquire() as conn:
        return await conn.fetchval("""
                                   INSERT INTO messages(chat_id, user_id, text)
                                   VALUES ($1, $2, $3)
                                   RETURNING id;
                                   """, chat_id, user_id, text)


async def get_messages(chat_id: int, limit: int = 50) -> List[MessageModel]:
    async with db.pool.pool.acquire() as conn:
        records = await conn.fetch("""
                                   SELECT m.id,
                                          m.chat_id,
                                          m.user_id,
                                          u.username,
                                          u.first_name,
                                          u.last_name,
                                          m.text,
                                          m.created_at
                                   FROM messages m
                                            LEFT JOIN users u ON m.user_id = u.id
                                   WHERE m.chat_id = $1
                                   ORDER BY m.created_at DESC
                                   LIMIT $2;
                                   """, chat_id, limit)

        return [MessageModel(**dict(r)) for r in records]


async def delete_messages(chat_id: int):
    async with db.pool.pool.acquire() as conn:
        await conn.exec("""
                                   DELETE
                                   FROM messages m
                                   WHERE m.chat_id = $1;
                                   """, chat_id)
