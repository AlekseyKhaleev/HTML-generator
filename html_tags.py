from abc import ABC, abstractmethod
from itertools import cycle, repeat
from typing import Iterator

HTML_SINGLES = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta',
                'param', 'source', 'track', 'wbr'}

HTML_DOUBLES = {"a", "abbr", "address", "article", "aside", "audio", "b", "bdi", "bdo", "blockquote", "button",
                "canvas", "caption", "cite", "code", "data", "datalist", "dd", "del", "details", "dfn", "div", "dl",
                "dt", "em", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6",
                "hgroup", "i", "iframe", "ins", "kbd", "label", "legend", "li", "map", "mark", "menu", "menuitem",
                "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "pre", "progress", "q",
                "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "small", "span", "strong", "style",
                "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "title",
                "tr", "u", "ul", "var", "video"}

HTML_UNIQUES = {"html", "head", "body", "header", "main", "footer"}


class HtmlTag(ABC):
    def __init__(self, tag_name: str):
        self.__tag_name = tag_name
        self.tag = tag_name

    def __repr__(self):
        return f"{type(self).__name__}({self.__tag_name})"

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
    """ This class is used to implement "flyweight" pattern """
    __instances: dict[str, HtmlTag] = dict()

    def __new__(cls, tag_name: str, *args, **kwargs):
        return cls.__instances.setdefault(tag_name, super().__new__(cls))


class TagContent(SingleTag):

    def _get_tag_gen(self, tag_name: str) -> Iterator:
        return repeat(tag_name)
