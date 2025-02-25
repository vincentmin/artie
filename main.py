import chainlit as cl
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from utils import respond, display_sidebar, initiate_conversation
from config_rijks import RijksConfig
from config_moma import MomaConfig
from config_tate import TateConfig

# Instantiate configs only once for memory efficiency
rijks_config = RijksConfig()
moma_config = MomaConfig()
tate_config = TateConfig()


client = genai.Client()
model_id = "gemini-2.0-flash-001"

google_search_tool = Tool(google_search=GoogleSearch())


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: dict[str, str],
    default_user: cl.User,
) -> cl.User | None:
    return default_user


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Rijks Museum",
            markdown_description="Praat met Artie over kunstwerken van het Rijks Museum",
            icon="https://iiif.micr.io/PJEZO/pct:0.56,0.48,0.11,0.1325/512,/0/default.jpg",
        ),
        cl.ChatProfile(
            name="MoMA",
            markdown_description="Talk to Artie about art pieces from the MoMA",
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
    languages = cl.user_session.get("languages", "").split(";")
    language = languages[0] if languages else "en"
    default_chat_profile = (
        "Rijks Museum" if "nl-BE" in language or "nl-NL" in language else "MoMA"
    )
    chat_profile = cl.user_session.get("chat_profile", default_chat_profile)
    match chat_profile:
        case "Rijks Museum":
            config = rijks_config
        case "MoMA":
            config = moma_config
        case "Tate":
            config = tate_config
        case _:
            raise ValueError(f"Invalid chat profile: {chat_profile}")

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
    record = config.get_next_record()

    await display_sidebar(record, config.side_bar_prompt)
    await initiate_conversation(record, config.init_conversation_prompt)


@cl.on_message
async def main(message: cl.Message):
    chat = cl.user_session.get("chat")
    if not chat:
        return await cl.Message(
            content="Artie is inspecting the art piece and should soon send you his thoughts. Please be patient until then. You can refresh the page if Artie is taking too long."
        ).send()
    await respond(message.content)
