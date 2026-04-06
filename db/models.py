from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class MessageModel(BaseModel):
    id: int
    chat_id: int
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    text: Optional[str] = None
    created_at: datetime

class UserModel(BaseModel):
    id: int
    peer_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class ChatModel(BaseModel):
    id: int
    peer_id: int
    title: Optional[str] = None