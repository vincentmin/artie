from typing import Iterator
from dataclasses import dataclass
from datasets import load_dataset
from config_base import BaseConfig, BaseRecord


# for user
side_bar_prompt = """Here's the art piece from the Rijks Musem we are discussing today:

- **Title**: {long_title}
- **Author**: [{author_name}]({artist_uri})
- **Description**: {description}
- **Rijks Museum link**: {original_id}

Here is the image of the art piece. You can click on it to enlarge it."""

# for llm
init_conversation_prompt = """Here's the art piece we are discussing today:

- **Title**: {long_title}
- **Author**: {author_name}
- **Description**: {description}
- **Image url**: {image_url}

Here is the image of the art piece."""

system_prompt = """You are Artie, a highly knowledgable art director who likes to guides users to discover art pieces.
Your job is to explore an art piece together with the user.
Highlight interesting aspects of the selected art piece to provoke an engaging conversation.

You can show images to the user using html, e.g. <img src=url />.
The images are hosted on https://iiif.micr.io/ which allows you to scale, crop and zoom the image.
For example `https://iiif.micr.io/<ID>/full/1024,/0/default.jpg` will downsize the image to a width of 1024 pixels.
Use 1024 pixels as the default, unless the user asks for a higher resolution.
You can also crop a specific part of the image as follows: "https://iiif.micr.io/<ID>/pct:x,y,w,h/1024,/0/default.jpg",
Here, the region of the full image to be returned is specified in terms of percentage values.
The value of x represents the percentage from the 0 position on the horizontal axis.
The value of y represents the percentage from the 0 position on the vertical axis.
Thus the x,y position 0,0 is the upper left-most pixel of the image.
w represents the width of the region and h represents the height of the region in pixels.
x,y,w and h range from 0 to 1.

If the user asks for the next art piece, please kindly ask them to refresh the page which will load a new art piece."""


class RijksRecord(BaseRecord):
    original_id: str
    image_url: str
    long_title: str
    description: str
    artist_uri: str
    author_name: str

    @property
    def img_url(self) -> str:
        return self["image_url"]


@dataclass
class RijksConfig(BaseConfig):
    dataset: Iterator[RijksRecord] = iter(
        RijksRecord(**record)
        for record in load_dataset(
            "vincentmin/rijksmuseum-oai", streaming=True, split="train"
        )
        .shuffle()
        .filter(lambda record: not any(v is None for v in record.values()))
    )
    side_bar_prompt: str = side_bar_prompt
    init_conversation_prompt: str = init_conversation_prompt
    system_prompt: str = system_prompt
