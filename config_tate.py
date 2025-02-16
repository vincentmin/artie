from typing import Iterator
from dataclasses_json import dataclass_json
from dataclasses import dataclass
from datasets import load_dataset
from config_base import BaseConfig, BaseRecord


# for user
side_bar_prompt = """Here's the art piece from the Tate that we are discussing today:

- **Title**: {title}
- **Artist**: {artist}
- **Tate link**: {url}

Here is the image of the art piece. You can click on it to enlarge it.
Select another chat profile to switch museums or language and refresh the page to get a new art piece."""

# for llm
init_conversation_prompt = """Here's the art piece from the Tate that we are discussing today:

- **Title**: {title}
- **Artist**: {artist}
- **Image url**: {thumbnailUrl}

Here is the image of the art piece."""

system_prompt = """You are Artie, a highly knowledgable art director at the Tate who likes to guides users to discover art pieces.
Your job is to explore an art piece together with the user.
Highlight interesting aspects of the selected art piece to provoke an engaging conversation.
You can show images to the user using html, e.g. <img src=url />.
If the user asks for the next art piece, please kindly ask them to refresh the page which will load a new art piece."""


@dataclass_json
@dataclass
class TateRecord(BaseRecord):
    id: str
    accession_number: str
    artist: str
    artistRole: str
    artistId: str
    title: str
    dateText: str
    medium: str | None
    creditLine: str | None
    year: str | None
    acquisitionYear: str | None
    dimensions: str | None
    width: str | None
    height: str | None
    depth: str | None
    units: str | None
    inscription: str | None
    thumbnailCopyright: str | None
    thumbnailUrl: str
    url: str

    @property
    def img_url(self) -> str:
        return self.thumbnailUrl


def dataset() -> Iterator[TateRecord]:
    """We need to loop infinitely to avoid StopIteration errors"""
    while True:
        finite_dataset: Iterator[TateRecord] = iter(
            TateRecord.from_dict(record)
            for record in load_dataset("vincentmin/tate", streaming=True, split="train")
            .filter(
                lambda record: (
                    record.get("thumbnailUrl", False)
                    and record.get("artist", False)
                    and record.get("title", False)
                    and record.get("url", False)
                )
            )
            .shuffle()
        )
        for record in finite_dataset:
            yield record


@dataclass
class TateConfig(BaseConfig):
    dataset: Iterator[TateRecord] = dataset()
    side_bar_prompt: str = side_bar_prompt
    init_conversation_prompt: str = init_conversation_prompt
    system_prompt: str = system_prompt
