from abc import ABC, abstractmethod
from itertools import cycle, repeat, chain
from enum import Enum
from typing import Iterator, Generator
from functools import wraps


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


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


SINGLE_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param',
               'source', 'track', 'wbr'}

DOUBLE_TAGS = {"a", "abbr", "address", "article", "aside", "audio", "b", "bdi", "bdo", "blockquote", "button", "canvas",
               "caption", "cite", "code", "data", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt", "em",
               "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "i",
               "iframe", "ins", "kbd", "label", "legend", "li", "map", "mark", "menu", "menuitem", "meter", "nav",
               "noscript", "object", "ol", "optgroup", "option", "output", "p", "pre", "progress", "q", "rp", "rt",
               "ruby", "s", "samp", "script", "section", "select", "small", "span", "strong", "style", "sub", "summary",
               "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "u", "ul",
               "var", "video"}

SINGLETONES = {"html", "head", "body", "header", "main", "footer"}


def create_tag_type(tag_name: str) -> type(HtmlTag):
    def change_init(type_name: str):
        def __init__(self, *args, **kwargs):
            super(type(self), self).__init__(type_name, *args, **kwargs)
        return __init__

    if tag_name in SINGLE_TAGS:
        return type(tag_name, (SingleTag,), {"__init__": change_init(tag_name)})

    elif tag_name in DOUBLE_TAGS:
        return type(tag_name, (DoubleTag,), {"__init__": change_init(tag_name)})

    elif tag_name in SINGLETONES:
        return type(tag_name, (DoubleTag, Singleton,), {"__init__": change_init(tag_name)})

    else:
        raise ValueError(f"Wrong tag name: {tag_name}\n This is not html tag")
