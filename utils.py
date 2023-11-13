from abc import ABC, ABCMeta, abstractmethod
from enum import IntEnum
from itertools import cycle, repeat
from typing import Iterator

from PySide6.QtCore import QObject


class _ABCQObjectMeta(type(QObject), ABCMeta): ...


class HtmlWidget(QObject, ABC, metaclass=_ABCQObjectMeta):
    @property
    @abstractmethod
    def sections(self):
        pass

    @property
    @abstractmethod
    def divs(self):
        pass

    @property
    @abstractmethod
    def inline(self):
        pass


# стратегия (поведенческий)
class HtmlBuildStrategy:
    def __init__(self, *, bordered):
        # self.builder =
        pass

    # адаптер (структурный)
    def build_page(self, obj: HtmlWidget):
        return self.builder.generate_html(obj.sections, obj.divs, inline=obj.inline)


class HtmlTag(ABC):
    __instances = dict()

    def __new__(cls, tag_name, *args, **kwargs):
        return cls.__instances.setdefault(tag_name, super().__new__(cls))

    def __init__(self, tag_name: str):
        self.tag_iter = self._get_tag_iter(tag_name)
        self._states = cycle(IntEnum("State", "CLOSED OPEN"))
        self.state = self._states.__next__()

    @property
    @abstractmethod
    def tag(self) -> str: ...

    @abstractmethod
    def _get_tag_iter(self, tag_name: str) -> Iterator[str]:
        pass


class SimpleTag(HtmlTag):
    @property
    def tag(self) -> str:
        return next(self.tag_iter)

    def _get_tag_iter(self, tag_name: str) -> Iterator:
        return repeat(f"<{tag_name}>")


class DoubleTag(HtmlTag):
    @property
    def tag(self) -> str:
        self.state = next(self._states)
        return next(self.tag_iter)

    def _get_tag_iter(self, tag_name) -> Iterator:
        return cycle((f"<{tag_name}>", f"</{tag_name}>"))


class PageBuilder:
    def build_tag(self ):
        pass


# def build_base(self):

div = DoubleTag("div")
img = SimpleTag("img")

for _ in range(4):
    print(div.tag)
    print(img.tag)
    print(div.tag)
