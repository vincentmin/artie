from typing import cast
from PIL import Image
import aiohttp
import io
import chainlit as cl
from google.genai.types import PartUnionDict, GenerateContentResponse
from google.genai.chats import AsyncChat
from config_base import BaseRecord, BaseConfig
from config_moma import MomaConfig
from config_rijks import RijksConfig


def get_config(chat_profile: str) -> BaseConfig:
    match chat_profile:
        case None:
            return RijksConfig()
        case "Rijks Museum":
            return RijksConfig()
        case "MOMA":
            return MomaConfig()
        case _:
            raise ValueError(f"Invalid chat_profile: {chat_profile}")


async def _load_image(url: str) -> Image.Image:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            image_bytes = await response.read()
            image = Image.open(io.BytesIO(image_bytes))
            return image


async def load_image(url: str) -> Image.Image:
    """Load an image in 1024px width resolution keeping the aspect ratio"""
    return await _load_image(
        url.replace("/full/max/0/default.jpg", "/full/1024,/0/default.jpg")
    )


async def respond(text: PartUnionDict | list[PartUnionDict]):
    # Fetch chat session for current user
    chat: AsyncChat = cl.user_session.get("chat")
    # Stream response
    msg = cl.Message(content="")
    async for chunk in await chat.send_message_stream(message=text):
        chunk = cast(GenerateContentResponse, chunk)
        await msg.stream_token(chunk.text)

    # Display grounding context as elements.
    elements = []
    for candidate in chunk.candidates:
        if (
            (c := candidate.grounding_metadata)
            and (sep := c.search_entry_point)
            and (rc := sep.rendered_content)
        ):
            elements.append(cl.Text(name="sources", content=rc, display="inline"))
    msg.elements = elements

    await msg.send()


async def display_sidebar(record: BaseRecord, prompt: str):
    text = prompt.format(**record.to_dict())
    elements = [
        cl.Text(content=text, name="art piece", display="side"),
        cl.Image(url=record.img_url, name="image", display="side"),
    ]
    await cl.ElementSidebar.set_elements(elements)
    await cl.ElementSidebar.set_title("Art Piece")


async def initiate_conversation(record: BaseRecord, prompt: str):
    text = prompt.format(**record.to_dict())
    image = await load_image(record.img_url)
    await respond([text, image])
