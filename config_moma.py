from typing import Iterator
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from datasets import load_dataset
from config_base import BaseConfig, BaseRecord


# for user
side_bar_prompt = """Here's the art piece we are discussing today:

- **Title**: {Title}
- **Artist**: {Artist}
- **MOMA link**: {URL}

Here is the image of the art piece. You can click on it to enlarge it."""

# for llm
init_conversation_prompt = """Here's the art piece we are discussing today:

- **Title**: {Title}
- **Artist**: {Artist}
- **Image url**: {ImageURL}

Here is the image of the art piece."""

system_prompt = """You are Artie, a highly knowledgable art director who likes to guides users to discover art pieces.
Your job is to explore an art piece together with the user.
Highlight interesting aspects of the selected art piece to provoke an engaging conversation.
You can show images to the user using html, e.g. <img src=url />.
If the user asks for the next art piece, please kindly ask them to refresh the page which will load a new art piece."""


@dataclass_json
@dataclass
class MomaRecord(BaseRecord):
    Title: str
    Artist: list[str]
    ArtistBio: list[str]
    Nationality: list[str]
    BeginDate: list[str]
    EndDate: list[str]
    Gender: list[str]
    Date: str | None
    Medium: str | None
    Dimensions: str | None
    CreditLine: str | None
    AccessionNumber: str
    Classification: str
    Department: str
    DateAcquired: str | None
    Cataloged: str
    ObjectID: int
    URL: str
    ImageURL: str
    OnView: str

    @property
    def img_url(self) -> str:
        return self.ImageURL


def dataset() -> Iterator[MomaRecord]:
    """We need to loop infinitely to avoid StopIteration errors"""
    while True:
        finite_dataset: Iterator[MomaRecord] = iter(
            MomaRecord.from_dict(record)
            for record in load_dataset("vincentmin/moma", streaming=True, split="train")
            .shuffle()
            .filter(
                lambda record: (
                    record.get("Title", False)
                    and record.get("Artist", False)
                    and record.get("ImageURL", False)
                    and record.get("URL", False)
                )
            )
        )
        for record in finite_dataset:
            yield record


@dataclass
class MomaConfig(BaseConfig):
    dataset: Iterator[MomaRecord] = dataset()
    side_bar_prompt: str = side_bar_prompt
    init_conversation_prompt: str = init_conversation_prompt
    system_prompt: str = system_prompt
