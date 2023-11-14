from abc import ABC, ABCMeta, abstractmethod
from enum import IntEnum
from itertools import cycle, repeat, zip_longest, chain
from typing import Iterator, Self
from collections import deque

from PySide6.QtCore import QObject

qobj_meta = type(QObject)


class _ABCQObjectMeta(qobj_meta, ABCMeta): ...


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
    # def build_page(self, obj: HtmlWidget):
    #     return self.builder.generate_html(obj.sections, obj.divs, inline=obj.inline)


class State(IntEnum):
    CLOSED = 0
    OPEN = 1


class HtmlTag(ABC):

    def __init__(self, tag_name: str):
        self._tag_iter = self._get_tag_iter(tag_name)
        self._states = cycle(State)
        self.state = self._states.__next__()
        self.next_calls_number = 0

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self): ...

    def __str__(self):
        return self.__next__()

    @property
    def max_calls_number(self):
        return 100

    @abstractmethod
    def _get_tag_iter(self, tag_name: str) -> Iterator[str]:
        pass


class SimpleTag(HtmlTag):

    def __next__(self):
        if self.next_calls_number == self.max_calls_number:
            self.next_calls_number = 0
            raise StopIteration
        self.next_calls_number += 1
        return next(self._tag_iter)

    def _get_tag_iter(self, tag_name: str) -> Iterator:
        return repeat(f"<{tag_name}>")


class DoubleTag(HtmlTag):
    def __next__(self):
        self.state = next(self._states)
        return next(self._tag_iter)

    def _get_tag_iter(self, tag_name) -> Iterator:
        return cycle((f"<{tag_name}>", f"</{tag_name}>"))


class AbstractBuilder(ABC):
    def __init__(self):
        self.stack = deque()

    @abstractmethod
    def add(self, tag: HtmlTag):
        pass


class TagBuilder(AbstractBuilder):
    pass


class BlockBuilder(AbstractBuilder):
    pass


class PageBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.res = str(SimpleTag("!DOCTYPE html"))
        self.indent_level = 0

    def add_tag(self, tag: HtmlTag, *, deep: bool = False):
        if not deep:
            if self.stack:
                self.res += f"\n{'    ' * self.indent_level}{str(self.stack.pop())}"
            self.res += f"\n{'    ' * self.indent_level}{str(tag)}"
            self.stack.append(tag)
        else:
            self.indent_level += 1
            self.res += f"\n{'    ' * self.indent_level}{str(tag)}"
            self.stack.append(tag)

    def add_content(self, content: str):
        if not self.stack:
            raise ValueError("Stack is empty, cannot add string-content")
        self.res += f"\n{'    ' * self.indent_level}{content}"

    def get_result(self):
        while self.stack:
            self.res += f"\n{'    ' * self.indent_level}{str(self.stack.pop())}"
            self.indent_level -= 1
        return self.res


# def build_base(self):

builder = PageBuilder()

builder.add_tag(DoubleTag("html"))
builder.add_tag(DoubleTag("head"), deep=True)
builder.add_tag(DoubleTag("body"))
builder.add_tag(DoubleTag("section"), deep=True)
builder.add_tag(DoubleTag("div"), deep=True)
builder.add_tag(DoubleTag("h1"), deep=True)
builder.add_content("This is h1 content")
builder.add_tag(DoubleTag("div"))
builder.add_tag(DoubleTag("section"))
builder.add_tag(DoubleTag("div"), deep=True)
print(builder.get_result())
