from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db, get_current_user
import crud.message as crud
import crud.chat as chat_crud
from schemas.message import Message, MessageInDB
from core.broker.redis import redis

import json

router = APIRouter(prefix="/message")


@router.get("/", response_model=MessageInDB)
async def get_message(message_id, db=Depends(get_db)):  # user_id=Depends(get_current_user)
    """Получить сообщение по заданному chat_id"""
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return message


@router.get("/allMy", response_model=(MessageInDB))
async def get_all_messages(user_id=Depends(get_current_user), db=Depends(get_db)):
    """Получить все сообщения пользователя"""
    messages = crud.get_all_messages_by_user(db=db, user_id=user_id)
    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return messages


@router.get("/allInChat", response_model=MessageInDB)
async def get_all_messages(chat_id: int, db=Depends(get_db)):
    """Получить все сообщения пользователя"""
    messages = crud.get_all_messages_in_chat(db=db, chat_id=chat_id)
    if messages is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return messages


@router.post("/", response_model=MessageInDB)
async def create_message(message: Message, db=Depends(get_db)):
    """Отправить сообщение"""
    result = crud.create_message(db=db, message=message)
    await redis.publish(f"chat-{message.chat_id}", result.toJSON())
    return result


@router.delete("/")
async def delete_message(message_id: int, db=Depends(get_db)):
    """Удалить сообщение"""
    message = crud.get_message_by_id(db=db, message_id=message_id)
    await redis.publish(f"chat-{message.chat_id}", f"DELETE-{message.id}")
    crud.delete_message(db=db, message_id=message_id)


@router.put("/", response_model=MessageInDB)
async def edit_message(message: MessageInDB, db=Depends(get_db)):
    """Изменить сообщение"""
    message_db = crud.edit_message(db=db, message=message)
    await redis.publish(f"chat-{message.chat_id}", f"EDIT-{message.id}")
    return message_db
