import requests
import asyncio
import logging
from io import BytesIO
from PIL import Image
from google import genai
from google.genai import types
from pydantic import BaseModel

# Things seem to break if we add google search. Turning it off for now.
# google_search_tool = types.Tool(google_search=types.GoogleSearch())

logger = logging.getLogger(__name__)

client = genai.Client()
model_name = "gemini-2.0-flash"
url = "https://iiif.micr.io/PJEZO/full/512,/0/default.jpg"
im = Image.open(BytesIO(requests.get(url).content))


def reconstruct_url(url: str, bbox: dict) -> str:
    return url.replace(
        "/full/",
        f"/pct:{bbox['x']:.3f},{bbox['y']:.3f},{bbox['w']:.3f},{bbox['h']:.3f}/",
    )


class BoundingBox(BaseModel):
    """
    Represents a bounding box with its 2D coordinates and associated label.

    Attributes:
        box_2d (list[int]): A list of integers representing the 2D coordinates of the bounding box,
                            typically in the format [x_min, y_min, x_max, y_max].
        label (str): A string representing the label or class associated with the object within the bounding box.
    """

    box_2d: list[int]
    label: str

    def convert(self) -> dict:
        # normalize and bound the values
        # The model often outputs more than 4 values ???
        y1, x1, y2, x2 = self.box_2d[:4]
        # convert to x, y, w, h
        return {
            "x": min(max(0, x1 / 1000), 1),
            "y": min(max(0, y1 / 1000), 1),
            "w": min(max(0, (x2 - x1) / 1000), 1),
            "h": min(max(0, (y2 - y1) / 1000), 1),
        }

    def to_tool_response(self, url: str) -> str:
        print("bbox", self.box_2d)
        response = f"{self.label}: {reconstruct_url(url, self.convert())}"
        print("Response", response)
        return response


class BoundingBoxes(BaseModel):
    boxes: list[BoundingBox]

    def to_tool_response(self, url: str) -> str:
        if not self.boxes:
            return "No objects found."
        return "\n".join([bbox.to_tool_response(url) for bbox in self.boxes])


# System prompt taken from google documentation: https://cloud.google.com/vertex-ai/generative-ai/docs/bounding-box-detection
config = types.GenerateContentConfig(
    system_instruction="""
Return bounding boxes as an array with labels.
Never return masks. Limit to 25 objects.
If an object is present multiple times, give each object a unique label
according to its distinct characteristics (colors, size, position, etc..).
""".strip(),
    temperature=0.5,
    response_mime_type="application/json",
    response_schema=BoundingBoxes,
)


# Tool for llm
def search_in_image(objects: str) -> str:
    """Search for an object in the image, for example a person, a face, a house. In case the image contains multiple similar objects, make sure to specify unique characteristics."""
    print("Searching for", objects)
    try:
        prompt = f"Detect the 2d bounding boxes for the following query: {objects}."
        response = client.models.generate_content(
            model=model_name,
            contents=[im, prompt],
            config=config,
        )
        return response.parsed.to_tool_response(url)
    except Exception as e:
        logger.error(e)
        return "Sorry, I couldn't find any objects in the image."


async def llm(contents: list):
    response = await client.aio.models.generate_content(
        model=model_name,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction="""You are Artie, an art director at the Rijks Museum. Use your tools to answer the user requests. You can show images to the user with html, e.g. <img src=url />""",
            tools=[search_in_image],  # , google_search_tool],
            # automatic_function_calling=types.AutomaticFunctionCallingConfig(
            #     disable=True,
            #     maximum_remote_calls=None,
            # ),
        ),
    )

    # If manually calling the tool
    # if response.function_calls:
    #     print(f"Function calls: {response.function_calls}")
    #     next_contents = [*contents, *[c.content for c in response.candidates]]
    #     for call in response.function_calls:
    #         try:
    #             tool_response = await search_in_image(
    #                 **(call.args if call.args else {})
    #             )
    #             tool_response = {"result": tool_response}
    #         except Exception as e:
    #             logger.error(e)
    #             tool_response = {"error": str(e)}
    #         next_contents.append(
    #             types.Content(
    #                 role="tool",
    #                 parts=[
    #                     types.Part.from_function_response(
    #                         name=call.name, response=tool_response
    #                     )
    #                 ],
    #             )
    #         )
    #     return await llm(next_contents)
    # elif response.text:
    #     text = response.text
    #     return text

    return response.text


async def main():
    prompt = "What do you think about the person in the center of the image with the black hat? Can you show me their face?"

    response = await llm([prompt, im])
    print("Final Response", response)


asyncio.run(main())
