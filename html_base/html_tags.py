from abc import ABC, abstractmethod
from itertools import cycle, repeat
from typing import Iterator


class HtmlTag(ABC):
    def __init__(self, tag_name: str):
        self.__tag_name = tag_name
        self.tag = tag_name

    def __repr__(self):
        return f"{type(self).__name__}({self.__tag_name})"

    def __hash__(self):
        return hash(self.__tag_name)

    def __eq__(self, other):
        if not isinstance(other, HtmlTag):
            return NotImplemented
        return self.__tag_name == other.__tag_name

    @abstractmethod
    def _get_tag_gen(self, tag_name: str) -> Iterator: ...

    @property
    def tag(self) -> str:
        return next(self._tag_iter)

    @tag.setter
    def tag(self, tag_name: str):
        self._tag_iter = self._get_tag_gen(tag_name)


class SingleTag(HtmlTag):
    def _get_tag_gen(self, tag_name: str) -> Iterator:
        return repeat(f"<{tag_name}>")


class DoubleTag(HtmlTag):
    def _get_tag_gen(self, tag_name: str) -> Iterator:
        return cycle((f"<{tag_name}>", f"</{tag_name}>"))


# singleton
class UniqueTag(DoubleTag):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance



