from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from typing import Any, Union

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


class HtmlAdapter:
    """ This class is used to implement the "adapter" pattern"""

    def __init__(self, *, bordered=False):
        self.director = HtmlDirector()

    def build_page(self, obj: HtmlWidget):
        self.director.build_tree(sections_num=obj.sections, divs_num=obj.divs, inline=obj.inline)

    def get_html(self):
        return self.director.get_html()


class Strategy(ABC):
    """ This class is a head of hierarchy, that provide to implement a part of the strategy pattern"""

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
    """ This class is used to implement those patterns:
        - factory method
        - builder
        - strategy (a part of)
        - state
    """

    def __init__(self) -> None:
        self.tree: list[Any] = list()
        self.branch_ptr: list[Any] = self.tree
        self.node_stack: UniqueStack = UniqueStack()

    def add(self, value: str, *, strategy: type[Strategy], specs: str = "") -> None:
        """ Implements a part of "strategy" pattern"""
        self.node_stack.add(self.branch_ptr)
        content = self.create_content(value, specs)  # a part of "factory method" pattern
        self.branch_ptr = strategy.add(self.branch_ptr, content)

    @staticmethod
    def create_content(value: str, specs: str) -> HtmlTag:
        """ Implements "factory method" pattern"""
        if value in HTML_SINGLES:
            return SingleTag(value, tag_specs=specs)
        elif value in HTML_DOUBLES:
            return DoubleTag(value, tag_specs=specs)
        elif value in HTML_UNIQUES:
            return UniqueTag(value, tag_specs=specs)
        else:
            return TagContent(value)

    def to_previous(self) -> "HtmlBuilder":
        """ Implements "state" pattern - we can return to previous state using node callstack"""
        if self.node_stack:
            last_branch = self.node_stack.pop()
            if last_branch is self.branch_ptr:
                self.to_previous()  # recursive call
            else:
                self.branch_ptr = last_branch
            if not self.node_stack:
                self.node_stack.add(self.branch_ptr)
        return self


class HtmlDirector:
    def __init__(self):
        self.builder = HtmlBuilder()

    def build_tree(self, *, sections_num, divs_num, inline=False) -> None:
        self.builder.add("!DOCTYPE", strategy=Leaf, specs="html")
        self.builder.add("html", strategy=Node)
        self.builder.add("head", strategy=Leaf)
        self.builder.add("body", strategy=Node)
        self.builder.add("header", strategy=Leaf)
        self.builder.add("main", strategy=Node)
        for s_num in range(1, sections_num + 1):
            self.builder.add("section", strategy=Node)
            for d_num in range(1, divs_num + 1):
                self.builder.add("div", strategy=Node)
                self.builder.add(f"section-{s_num} div-{d_num} message", strategy=Leaf)
                self.builder.to_previous()
            self.builder.to_previous()

    def get_html(self) -> str:
        res = ""
        space_tab = "    "

        def tree_traversal(node: list[Union[HtmlTag, Any]], level=-1) -> None:
            """ It's a function that traverses the html tree recursively to write result to nonlocal res variable """
            nonlocal res
            first_tag = node[0]
            res += space_tab * level + first_tag.tag + '\n'
            for child in node[1:]:
                match child:
                    case SingleTag():
                        res += space_tab * (level + 1) + child.tag + '\n'
                    case DoubleTag():
                        res += space_tab * (level + 1) + child.tag + child.tag + '\n'
                    case list():
                        tree_traversal(child, level + 1)  # recursive case
            if isinstance(first_tag, DoubleTag):
                res += space_tab * level + first_tag.tag + '\n'

        tree_traversal(self.builder.tree)
        return res


if __name__ == "__main__":
    director = HtmlDirector()
    director.build_tree(sections_num=2, divs_num=2)
    print(director.get_html())
