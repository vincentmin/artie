import chainlit as cl
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

client = genai.Client()
model_id = "gemini-2.0-flash-001"

google_search_tool = Tool(google_search=GoogleSearch())


@cl.step(type="tool")
async def tool():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"


@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    response = await client.aio.models.generate_content(
        model=model_id,
        contents=message.content,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
            # system_instruction="You are a helpful assistant",
        ),
    )

    await cl.Message(content=response.text).send()
    # response.candidates[0].grounding_metadata.search_entry_point.rendered_content
