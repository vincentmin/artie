from typing import Iterator
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseRecord:
    @property
    def img_url(self) -> str:
        raise NotImplementedError


class BaseConfig[T: BaseRecord]:
    dataset: Iterator[T]
    side_bar_prompt: str
    init_conversation_prompt: str
    system_prompt: str
