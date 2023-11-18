from abc import ABC, ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass
from typing import Any, Union

from PySide6.QtCore import QObject

from source.html_tags import HtmlTag, DoubleTag, SingleTag, UniqueTag, TagContent, HTML_SINGLES, HTML_DOUBLES, \
    HTML_UNIQUES


class _ABCQObjectMeta(type(QObject), ABCMeta): ...


class HtmlWidget(QObject, ABC, metaclass=_ABCQObjectMeta):
    @property
    @abstractmethod
    def sections(self) -> int: ...

    @property
    @abstractmethod
    def divs(self) -> int: ...

    @property
    @abstractmethod
    def bordered(self) -> bool: ...

    @property
    @abstractmethod
    def headers(self) -> bool: ...

    @property
    @abstractmethod
    def color(self) -> str: ...

    @property
    @abstractmethod
    def alignment(self) -> str: ...


@dataclass
class Style:
    name: str
    body: str


class HtmlAdapter:
    """ This class is used to implement the "adapter" pattern"""

    def __init__(self) -> None:
        self.director = HtmlDirector()

    def build_page(self, obj: HtmlWidget) -> None:
        style = self.create_style(color=obj.color, alignment=obj.alignment, bordered=obj.bordered)
        self.director.build_tree(sections_num=obj.sections, divs_num=obj.divs, div_style=style,
                                 headers=obj.headers)

    def get_html(self) -> str:
        return self.director.get_html()

    @staticmethod
    def create_style(*, color: str, alignment: str, bordered: bool, name: str = "container") -> "Style":
        style = f".{name} {{"
        if color:
            style += f"color: {color}; "
        if alignment:
            style += f"text-align: {alignment}; "
        if bordered:
            style += "border: 1px solid black; "
        style += "}"
        return Style(name, style)


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
        self.node_stack: deque = deque()

    def add(self, value: str, *, strategy: type[Strategy], specs: str = "") -> None:
        """ Implements a part of "strategy" pattern"""
        self.node_stack.append(self.branch_ptr)
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
                self.node_stack.append(self.branch_ptr)
        return self

    def get_result(self):
        return self.tree


class HtmlDirector:
    def __init__(self) -> None:
        self.html_builder = HtmlBuilder()

    def build_tree(self, *, sections_num: int, divs_num: int, div_style: Style, headers: bool) -> None:
        self.html_builder.add("!DOCTYPE", strategy=Leaf, specs="html")
        self.html_builder.add("html", strategy=Node)
        self.html_builder.add("head", strategy=Node)
        self.html_builder.add("style", strategy=Node, specs='type="text/css"')
        self.html_builder.add(div_style.body, strategy=Leaf)
        self.html_builder.to_previous().to_previous()
        self.html_builder.add("body", strategy=Node)
        self.html_builder.add("header", strategy=Leaf)
        self.html_builder.add("main", strategy=Node)
        for s_num in range(1, sections_num + 1):
            self.html_builder.add("section", strategy=Node)
            for d_num in range(1, divs_num + 1):
                self.html_builder.add("div", strategy=Node, specs=f"class={div_style.name}")
                if headers:
                    h_level = d_num if d_num <= 6 else 6
                    self.html_builder.add(f"h{h_level}", strategy=Node)
                    self.html_builder.add(f"section-{s_num} div-{d_num} message", strategy=Leaf)
                    self.html_builder.to_previous()
                else:
                    self.html_builder.add(f"section-{s_num} div-{d_num} message", strategy=Leaf)
                self.html_builder.to_previous()
            self.html_builder.to_previous()
        self.html_builder.to_previous()
        self.html_builder.add("footer", strategy=Leaf)

    def get_html(self) -> str:
        res = ""
        space_tab = "    "

        def tree_traversal(node: list[Union[HtmlTag, Any]], level: int = -1) -> None:
            """ It's a function that traverses the html tree recursively to write result to nonlocal "res" variable """
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

        tree_traversal(self.html_builder.tree)
        return res
