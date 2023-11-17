from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from typing import Any, Union
from sys import getsizeof
from PySide6.QtCore import QObject

from html_tags import HtmlTag, DoubleTag, SingleTag, UniqueTag, TagContent, HTML_SINGLES, HTML_DOUBLES, HTML_UNIQUES


class _ABCQObjectMeta(type(QObject), ABCMeta): ...


class UniqueStack:
    def __init__(self):
        self.stack = deque()
        self.images = set()

    def add(self, value):
        if id(value) not in self.images:
            self.stack.append(value)
            self.images.add(id(value))
        return self

    def pop(self):
        last = self.stack.pop()
        self.images.remove(id(last))
        return last


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
    def add(node: list[Any], value: HtmlTag) -> list[Any]:
        pass


class Node(Strategy):
    @staticmethod
    def add(node: list[Any], value: HtmlTag) -> list[Any]:
        if isinstance(value, DoubleTag):
            new_node = [value]
            node.append(new_node)
            return new_node
        else:
            return Leaf.add(node, value)


class Leaf(Strategy):
    @staticmethod
    def add(node: list[Any], value: HtmlTag) -> list[Any]:
        node.append(value)
        return node


class HtmlBuilder:
    def __init__(self):
        self.tree: list[Any] = list()
        self.branch_ptr: list[Any] = self.tree
        self.node_stack: UniqueStack = UniqueStack()

    def fill(self, value: str, *, strategy: type[Strategy]) -> None:
        self.node_stack.add(self.branch_ptr)
        content = self.create_content(value)
        self.branch_ptr = strategy.add(self.branch_ptr, content)

    @staticmethod
    def create_content(value: str) -> HtmlTag:
        if value in HTML_SINGLES:
            return SingleTag(value)
        elif value in HTML_DOUBLES:
            return DoubleTag(value)
        elif value in HTML_UNIQUES:
            return UniqueTag(value)
        else:
            return TagContent(value)

    @property
    def to_previous(self) -> "HtmlBuilder":
        for _ in range(2):
            if self.node_stack:
                self.branch_ptr = self.node_stack.pop()
        return self


class HtmlDirector:
    def __init__(self):
        self.builder = HtmlBuilder()

    def build_tree(self) -> None:
        self.builder.fill("<!DOCTYPE html>", strategy=Leaf)
        self.builder.fill("html", strategy=Node)
        self.builder.fill("head", strategy=Leaf)
        self.builder.fill("body", strategy=Node)
        self.builder.fill("header", strategy=Leaf)
        self.builder.fill("main", strategy=Node)
        self.builder.fill("section", strategy=Node)
        self.builder.fill("div", strategy=Node)
        self.builder.fill("section1 div1 message", strategy=Leaf)
        self.builder.to_previous.fill("div", strategy=Node)
        self.builder.fill("section1 div2 message", strategy=Leaf)

    def get_html(self) -> str:
        res = ""

        def tree_traversal(node: list[Union[HtmlTag, ...]], level=-1) -> None:
            nonlocal res
            first_tag = node[0]
            res += "\t" * level + first_tag.tag + '\n'
            for child in node[1:]:
                match child:
                    case SingleTag():
                        res += "\t" * (level + 1) + child.tag + '\n'
                    case DoubleTag():
                        res += "\t" * (level + 1) + child.tag + child.tag + '\n'
                    case list():
                        tree_traversal(child, level + 1)
            if isinstance(first_tag, DoubleTag):
                res += "\t" * level + first_tag.tag + '\n'

        tree_traversal(self.builder.tree)
        return res


if __name__ == "__main__":
    director = HtmlDirector()
    director.build_tree()
    print(director.get_html())
    print(f"{getsizeof(deque(range(10 ** 8)))} | {getsizeof(list(range(10 ** 8)))}")
