from typing import Iterator, TypedDict


class BaseRecord(TypedDict):
    @property
    def img_url(self) -> str:
        raise NotImplementedError


class BaseConfig:
    dataset: Iterator[BaseRecord]
    side_bar_prompt: str
    init_conversation_prompt: str
    system_prompt: str
