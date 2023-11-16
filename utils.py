from abc import ABC, ABCMeta, abstractmethod
from enum import IntEnum
from itertools import cycle, repeat, zip_longest, chain
from typing import Iterator, Self
from collections import deque

from PySide6.QtCore import QObject
from constants import STATE, MAX_CALLS, TAB
from html_tags import HtmlTag, DoubleTag, SingleTag, Singleton, create_tag_type


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
    # def build_page(self, obj: HtmlWidget):
    #     return self.builder.generate_html(obj.sections, obj.divs, inline=obj.inline)


class TreeBuilder(ABC):
    def __init__(self, *, tree: dict | None = None):
        self.tree = tree if tree is not None else dict()
        self.level = 0
        self.call_stack = deque()
        self.res = str()

    @abstractmethod
    def open_tag(self, tag: HtmlTag, *, inplace: bool = True): ...

    @abstractmethod
    def close_tag(self): ...

    @abstractmethod
    def add_value(self, value: str): ...


class TagBuilder(TreeBuilder):

    def add_inplace(self, tag: HtmlTag, key: DoubleTag) -> None:
        self.tree[key].append(tag)

    def add_nested(self, tag: HtmlTag, key: DoubleTag) -> None:
        self.tree[key].append({tag: []})

    def open_tag(self, tag: HtmlTag, *, inplace: bool = True):
        self.res += "\t" * self.level + tag.tag + "\n"
        self.call_stack.append(tag)
        self.level += 1

    def close_tag(self):
        self.level = 0 if self.level - 1 < 0 else self.level - 1
        last_tag = self.call_stack.pop()
        if isinstance(last_tag, DoubleTag):
            self.res += "\t" * self.level + last_tag.tag + "\n"

    def add_value(self, value: str):
        self.res += "\t" * self.level + value + "\n"

    def close_all(self):
        while self.call_stack:
            self.close_tag()


class HtmlDirector:
    def __init__(self):
        self.base_tree = {
            SingleTag("!DOCTYPE html"): {},
            DoubleTag("html"): {
                DoubleTag("head"): {},
                DoubleTag("body"): {
                    DoubleTag("header"): {},
                    DoubleTag("main"): [],
                    DoubleTag("footer"): {}
                }
            }
        }
        self.main_builder = TagBuilder(tree=self.base_tree[DoubleTag("html")][DoubleTag("body")])

    def build_tree(self, *, sections=1, divs=1):
        for _ in range(sections):
            self.main_builder.add_nested(DoubleTag("section"), DoubleTag("main"))
        for section in self.main_builder.tree[DoubleTag("main")]:
            for _ in range(divs):
                section[DoubleTag("section")].append(DoubleTag("div"))

    def result(self):
        return self.base_tree

div = create_tag_type("div")

tag = div()


print(div.tag)
