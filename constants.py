from dataclasses import dataclass
from enum import IntEnum
from itertools import chain, zip_longest


class STATE(IntEnum):
    CLOSED = 0
    OPEN = 1


class TAG_TYPE(IntEnum):
    SINGLE = 0
    DOUBLE = 1


@dataclass(frozen=True)
class TagInfo:
    name: str
    type: TAG_TYPE
    singleton: bool = False


TAB = "    "
MAX_CALLS = 100

SINGLE_TAGS = {'area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta',
               'param', 'source', 'track', 'wbr'}

DOUBLE_TAGS = {"a", "abbr", "address", "article", "aside", "audio", "b", "bdi",
               "bdo", "blockquote", "body", "button", "canvas", "caption", "cite", "code",
               "data", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt",
               "em", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2",
               "h3", "h4", "h5", "h6", "head", "header", "hgroup", "html", "i",
               "iframe", "ins", "kbd", "label", "legend", "li", "main", "map",
               "mark", "menu", "menuitem", "meter", "nav", "noscript", "object", "ol",
               "optgroup", "option", "output", "p", "pre", "progress", "q", "rp",
               "rt", "ruby", "s", "samp", "script", "section", "select", "small",
               "span", "strong", "style", "sub", "summary", "sup", "table", "tbody",
               "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr",
               "u", "ul", "var", "video"}
