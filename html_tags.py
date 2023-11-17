from abc import ABC, abstractmethod
from itertools import cycle, repeat
from typing import Iterator

HTML_SINGLES = {'!DOCTYPE', 'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link',
                'meta', 'param', 'source', 'track', 'wbr'}

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
    def __init__(self, tag_name: str, *, tag_specs: str = ""):
        self._tag_name = tag_name
        self._tag_specs = tag_specs
        self._tag_iter = self._get_tag_gen()

    def __repr__(self):
        return f"{type(self).__name__}({self._tag_name})"

    @abstractmethod
    def _get_tag_gen(self) -> Iterator: ...

    @property
    def tag(self) -> str:
        return next(self._tag_iter)


class SingleTag(HtmlTag):
    def _get_tag_gen(self) -> Iterator:
        return repeat(f"<{self._tag_name}{' ' * bool(self._tag_specs)}{self._tag_specs}>")


class DoubleTag(HtmlTag):
    def _get_tag_gen(self) -> Iterator:
        return cycle((f"<{self._tag_name}{' ' * bool(self._tag_specs)}{self._tag_specs}>", f"</{self._tag_name}>"))


# singleton
class UniqueTag(DoubleTag):
    """ This class is used to implement "flyweight" pattern """
    __instances: dict[str, HtmlTag] = dict()

    def __new__(cls, tag_name: str, *args, **kwargs):
        return cls.__instances.setdefault(tag_name, super().__new__(cls))


class TagContent(SingleTag):

    def _get_tag_gen(self) -> Iterator:
        return repeat(self._tag_name)
