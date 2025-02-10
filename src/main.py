from typing import TypedDict
import chainlit as cl
from datasets import load_dataset
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

client = genai.Client()
model_id = "gemini-2.0-flash-001"
system_prompt = """You are a highly knowledgable and extravert art director.
Your job is to entertain the user by highlighting interesting aspects
of the selected art piece and provoke an engaging conversation.
You can show images to the user using html, e.g. <img src=url />.
The images are hosted on https://iiif.micr.io/ which allows you to scale, crop and zoom the image.
For example `https://iiif.micr.io/<ID>/full/512,/0/default.jpg` will downsize the image to 512 pixels.
Use 512 pixels as the default, unless the user asks for a higher resolution.
You can also crop a specific part of the image as follows: "https://iiif.micr.io/<ID>/x,y,w,h/512,/0/default.jpg",
Here, the region of the full image to be returned is specified in terms of absolute pixel values.
The value of x represents the number of pixels from the 0 position on the horizontal axis.
The value of y represents the number of pixels from the 0 position on the vertical axis.
Thus the x,y position 0,0 is the upper left-most pixel of the image.
w represents the width of the region and h represents the height of the region in pixels.
Or use `pct:x,y,w,h` to provide percentages.
"""

google_search_tool = Tool(google_search=GoogleSearch())

ds = iter(
    load_dataset("vincentmin/rijksmuseum-oai", streaming=True, split="train")
    .shuffle()
    .filter(lambda record: not any(v is None for v in record.items()))
)


class Record(TypedDict):
    original_id: str
    image_url: str
    description: str
    artist_uri: str
    author_name: str


async def llm(text: str, system_instruction: str | None = None):
    system_instruction = system_instruction or system_prompt
    response = await client.aio.models.generate_content(
        model=model_id,
        contents=text,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
            system_instruction=system_instruction,
        ),
    )
    try:
        elements = [
            cl.Text(
                name="sources",
                content=response.candidates[
                    0
                ].grounding_metadata.search_entry_point.rendered_content,
                display="inline",
            )
        ]
    except Exception:
        elements = []
    print(response.text)
    return response, elements


@cl.on_chat_start
async def on_chat_start():
    record: Record = next(ds)
    response, elements = await llm(
        f"Here's the art piece we are discussing today: {record}"
    )
    await cl.Message(content=response.text, elements=elements).send()


@cl.on_message
async def main(message: cl.Message):
    response, elements = await llm(message.content)
    await cl.Message(content=response.text, elements=elements).send()
