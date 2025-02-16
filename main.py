import chainlit as cl
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from utils import respond, display_sidebar, initiate_conversation, get_config

client = genai.Client()
model_id = "gemini-2.0-flash-001"

google_search_tool = Tool(google_search=GoogleSearch())


# @cl.oauth_callback
# def oauth_callback(
#     provider_id: str,
#     token: str,
#     raw_user_data: dict[str, str],
#     default_user: cl.User,
# ) -> cl.User | None:
#     return default_user


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Rijks Museum",
            markdown_description="Praat met Artie over kunstwerken van het Rijks Museum",
            icon="https://iiif.micr.io/PJEZO/pct:0.56,0.48,0.11,0.1325/512,/0/default.jpg",
        ),
        cl.ChatProfile(
            name="MOMA",
            markdown_description="Talk to Artie about art pieces from the MOMA",
            icon="https://iiif.micr.io/PJEZO/pct:0.43,0.45,0.11,0.1325/512,/0/default.jpg",
        ),
        cl.ChatProfile(
            name="Tate",
            markdown_description="Talk to Artie about art pieces from the Tate",
            icon="https://iiif.micr.io/PJEZO/pct:0.275,0.575,0.08,0.0963/512,/0/default.jpg",
        ),
    ]


@cl.on_chat_start
async def on_chat_start():
    chat_profile = cl.user_session.get("chat_profile")
    config = get_config(chat_profile)

    # instantiate chat session to keep track of conversation
    chat = client.aio.chats.create(
        model=model_id,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
            system_instruction=config.system_prompt,
        ),
    )
    cl.user_session.set("chat", chat)

    # fetch random record
    record = next(config.dataset)

    await display_sidebar(record, config.side_bar_prompt)
    await initiate_conversation(record, config.init_conversation_prompt)


@cl.on_message
async def main(message: cl.Message):
    await respond(message.content)
