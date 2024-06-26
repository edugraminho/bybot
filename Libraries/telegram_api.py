from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from Variables.config import SESSION_DIRECTORY, MESSAGES_LIMIT
from Libraries.logger import get_logger
import os

"""
Para conseguir logar na sessao tem q entrar em https://my.telegram.org.
Pegar o ID e HASH 
Copiar o arquivo gerado e jogar no repo do robo

"""

API_ID = os.getenv("TEL_API_ID")
API_HASH = os.getenv("TEL_API_HASH")

logger = get_logger(__name__)


def get_messages_group():
    try:
        # logger.info(f"Buscando novos Sinais no Telegram")

        with TelegramClient(
            session=f"{SESSION_DIRECTORY}/session_name.session",
            api_id=API_ID,
            api_hash=API_HASH,
        ) as client:

            result = client(
                GetDialogsRequest(
                    offset_date=None,
                    offset_id=0,
                    offset_peer=InputPeerEmpty(),
                    limit=500,
                    hash=-0,
                )
            )
            title = "VIP CLUB | BybitPro"
            for chat in result.chats:

                if chat.title == title:
                    messages = client.get_messages(chat, limit=MESSAGES_LIMIT)

                    return messages

        # client.disconnect()
    except Exception as e:
        logger.error(f"Error get_messages_group: {e}")
        pass
