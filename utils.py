from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from typing import Any

from PySide6.QtCore import QObject

from html_tags import HtmlTag, DoubleTag, SingleTag, UniqueTag, HTML_SINGLES, HTML_DOUBLES, HTML_UNIQUES


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
# class HtmlBuildStrategy:
#     def __init__(self, *, bordered):
#         # self.builder =
#         pass
#
#     # адаптер (структурный)
#     def build_page(self, obj: HtmlWidget):
#         return self.builder.generate_html(obj.sections, obj.divs, inline=obj.inline)

class Strategy(ABC):
    @staticmethod
    @abstractmethod
    def add(node: list[Any], value: str) -> None:
        pass


class Node(Strategy):
    @staticmethod
    def add(node: list[Any], value: str | HtmlTag) -> list[Any]:
        if isinstance(value, DoubleTag):
            new_node = {value: []}
            node.append(new_node)
            return new_node[value]
        else:
            return Leaf.add(node, value)


class Leaf(Strategy):
    @staticmethod
    def add(node: list[Any], value: str) -> list[Any]:
        node.append(value)
        return node


class HtmlBuilder:
    def __init__(self):
        self.tree = dict()
        self.tree.setdefault("root", [])
        self.branch_ptr = self.tree["root"]
        self.node_stack = deque()

    @staticmethod
    def create_content(value: str) -> HtmlTag | str:
        if value in HTML_SINGLES:
            return SingleTag(value)
        elif value in HTML_DOUBLES:
            return DoubleTag(value)
        elif value in HTML_UNIQUES:
            return UniqueTag(value)
        else:
            return value

    def fill(self, value: str, *, strategy: type[Strategy], backward: bool = False) -> None:
        content = self.create_content(value)
        if backward:
            if self.node_stack:
                self.branch_ptr = self.node_stack.pop()
        self.branch_ptr = strategy.add(self.branch_ptr, content)

class HtmlDirector:
    def __init__(self):
        self.builder = HtmlBuilder()

    def build_html(self):
        self.builder.fill("<!DOCTYPE html>", strategy=Leaf)
        self.builder.fill("html", strategy=Node)
        self.builder.fill("head", strategy=Leaf)
        self.builder.fill("body", strategy=Node)
        self.builder.fill("header", strategy=Leaf)
        self.builder.fill("main", strategy=Node)
        self.builder.fill("section", strategy=Node)
        self.builder.fill("div", strategy=Node)
        self.builder.fill("section1 div1 message", strategy=Leaf)
        self.builder.fill("div", strategy=Node, backward=True)
        self.builder.fill("section1 div2 message", strategy=Leaf)
        self.builder.
        return self.builder.tree
