from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass, field
from collections import deque

from PySide6.QtCore import QObject

from html_base.html_tags import HtmlTag, DoubleTag, SingleTag, Singleton
from html_base.constants import HTML_SINGLES, HTML_DOUBLES, HTML_SINGLETONS


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


class Builder(ABC, Singleton):
    def add(self, value: str):
        content = self.create_content(value)

    @staticmethod
    # фабричный метод | стратегия
    def create_content(value: str) -> HtmlTag | str:
        if value in HTML_SINGLES:
            return SingleTag(value)
        elif value in HTML_DOUBLES:
            return DoubleTag(value)
        elif value in HTML_SINGLETONS:
            return type("HtmlSingleton", (DoubleTag, Singleton), {})(value)
        else:
            return value
