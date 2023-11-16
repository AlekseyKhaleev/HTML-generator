from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from typing import Any

from PySide6.QtCore import QObject

from html_tags import HtmlTag, DoubleTag, SingleTag, UniqueTag, HTML_SINGLES, HTML_DOUBLES, HTML_UNIQUES


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
    def add(node: list[Any], value: str) -> None:
        pass


class Node(Strategy):
    @staticmethod
    def add(node: list[Any], value: str | HtmlTag) -> list[Any]:
        if isinstance(value, DoubleTag):
            new_node = [value]
            node.append(new_node)
            return new_node
        else:
            return Leaf.add(node, value)


class Leaf(Strategy):
    @staticmethod
    def add(node: list[Any], value: str | HtmlTag) -> list[Any]:
        node.append(value)
        return node


class HtmlBuilder:
    def __init__(self):
        self.tree = list()
        self.branch_ptr = self.tree
        self.node_stack = UniqueStack()

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

    def fill(self, value: str, *, strategy: type[Strategy]) -> None:
        self.node_stack.add(self.branch_ptr)
        content = self.create_content(value)
        self.branch_ptr = strategy.add(self.branch_ptr, content)

    @property
    def to_previous(self):
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

        def tree_traversal(node: list[Any], level=-1):
            nonlocal res
            first = node[0]
            if isinstance(first, HtmlTag):
                res += "\t" * level + first.tag + '\n'
            for child in node[1:]:
                match child:
                    case SingleTag():
                        res += "\t" * (level + 1) + child.tag + '\n'
                    case DoubleTag():
                        res += "\t" * (level + 1) + child.tag + child.tag + '\n'
                    case str():
                        res += "\t" * (level + 1) + child + '\n'
                    case list():
                        tree_traversal(child, level + 1)
            if isinstance(first, DoubleTag):
                res += "\t" * level + first.tag + '\n'

        tree_traversal(self.builder.tree)
        return res


if __name__ == "__main__":
    director = HtmlDirector()
    director.build_tree()
    print(director.get_html())
