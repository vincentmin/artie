from typing import Callable, Iterator
import logging
from dataclasses import dataclass
from dataclasses_json import dataclass_json


logger = logging.getLogger(__name__)


@dataclass_json
@dataclass
class BaseRecord:
    @property
    def img_url(self) -> str:
        raise NotImplementedError


class BaseConfig[T: BaseRecord]:
    side_bar_prompt: str
    init_conversation_prompt: str
    system_prompt: str
    dataset: Iterator[T] | None = None

    @staticmethod
    def get_dataset() -> Iterator[T]:
        raise NotImplementedError

    def get_next_record(self) -> T:
        if self.dataset is None:
            self.dataset = self.get_dataset()
        try:
            return next(self.dataset)
        except Exception as e:
            logger.error(f"Error getting next record: {e}")
            self.dataset = self.get_dataset()
            return self.get_next_record()
