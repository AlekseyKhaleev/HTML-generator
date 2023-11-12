from functools import wraps
from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtCore import QObject


class _ABCQObjectMeta(type(QObject), ABCMeta): ...


# строитель (порождающий)
class HtmlBuilder:
    """
    Класс для построения HTML-тегов во вложенной структуре.

    Attributes:
        _tag (str): Имя тега HTML-элемента, который строится.
        _inline (bool): Определяет, должен ли HTML-элемент отображаться встроенным.

    Methods:
        __init__(self, tag: str, *, inline: bool = False) -> None:
            Инициализирует новый экземпляр класса HtmlBuilder.

        __enter__(self) -> 'HtmlBuilder':
            Входит в контекстный менеджер, открывая HTML-тег.

        __exit__(self, exc_type, exc_value, traceback) -> None:
            Выходит из контекстного менеджера, закрывая HTML-тег.

        fill(self, text: str) -> None:
            Заполняет HTML-элемент данным текстом.

        @classmethod
        def generate_html(cls, tag: str, content: str, *, inline: bool = False) -> str:
            Генерирует полный HTML-элемент с заданным количеством секций и тегов,
            а также с дополнительным атрибутом "inline".

    Пример использования:
        1. with HtmlBuilder('div') as builder:
               builder.fill('Привет, мир!')

        2. html = HtmlBuilder.generate_html('div', 'Hello, world!', inline=True)
           print(html)
    """
    _level = -1
    _accumulated_tags = ""

    # легковес (структурный)
    def __new__(cls, *args, **kwargs):
        instances = {}
        return instances.get(hash(args + tuple(kwargs.items())), super().__new__(cls))

    def __init__(self, tag: str, *, inline: bool = False) -> None:
        """
        Инициализирует новый экземпляр класса HtmlBuilder.

        Args:
            tag (str): Имя тега HTML-элемента, который строится.
            inline (bool, optional): Определяет, должен ли HTML-элемент отображаться встроенным.
                По умолчанию False.
        """
        self._tag = tag
        self._inline = inline

    def __enter__(self):
        """
        Входит в контекстный менеджер, открывая HTML-тег.

        Returns:
            HtmlBuilder: Экземпляр класса HtmlBuilder.
        """
        type(self)._level += 1
        type(self)._accumulated_tags += f"{'    ' * type(self)._level}<{self._tag}>" + ['\n', ''][self._inline]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Выходит из контекстного менеджера, закрывая HTML-тег.

        Args:
            exc_type: Тип исключения.
            exc_value: Значение исключения.
            traceback: Отслеживание исключения.
        """
        type(self)._accumulated_tags += f"{['    ' * type(self)._level, ''][self._inline]}</{self._tag}>\n"
        type(self)._level -= 1

    def fill(self, text):
        """
        Заполняет HTML-элемент данным текстом.

        Args:
            text (str): Текст для заполнения HTML-элемента.
        """
        type(self)._accumulated_tags += ['    ' * (type(self)._level + 1), ''][self._inline] + text + ['\n', ''][
            self._inline]

    @classmethod
    def generate_html(cls, sections=0, tags=0, *, inline=False):
        """
        Генерирует полный HTML-элемент с заданным количеством секций и тегов,
        а также с дополнительным атрибутом "inline".

        Args:
            sections (int, optional): Количество секций HTML-элемента.
                По умолчанию 0.
            tags (int, optional): Количество тегов HTML-элемента.
                По умолчанию 0.
            inline (bool, optional): Определяет, должен ли HTML-элемент отображаться встроенным.
                По умолчанию False.

        Returns:
            str: Сгенерированный HTML-код элемента.
        """

        cls._accumulated_tags += "<!DOCTYPE html>\n"
        with cls('html'):
            with cls('head'):
                pass
            with cls('body'):
                with cls('header', inline=True):
                    pass
                with cls('main'):
                    for sect_num in range(sections):
                        with cls('section'):
                            for tag_num in range(tags):
                                with cls('div', inline=inline) as div:
                                    div.fill(f"Section {sect_num + 1}, Div {tag_num + 1}")
                with cls("footer", inline=True):
                    pass
        result, cls._accumulated_tags = cls._accumulated_tags, ""
        return result


# декоратор (структурный)
def border_divs(cls: type[HtmlBuilder]) -> type[HtmlBuilder]:
    class HtmlBorderedBuilder(cls):
        pass

    old_enter = HtmlBorderedBuilder.__enter__
    old_exit = HtmlBorderedBuilder.__exit__

    @wraps(old_enter)
    def enter_wrapper(self):
        match self._tag:
            case 'head':
                res = old_enter(self)
                with HtmlBorderedBuilder('style') as style:
                    style.fill(".bordered { border: 2px solid black; }")
                return res
            case 'div':
                self._tag = 'div class="bordered"'
        return old_enter(self)

    @wraps(old_exit)
    def exit_wrapper(self, *args, **kwargs):
        if self._tag == 'div class="bordered"':
            self._tag = 'div'
        old_exit(self, *args, **kwargs)

    HtmlBorderedBuilder.__enter__ = enter_wrapper
    HtmlBorderedBuilder.__exit__ = exit_wrapper
    return HtmlBorderedBuilder


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
class HtmlBuildStrategy:
    def __init__(self, *, bordered):
        self.builder = border_divs(HtmlBuilder) if bordered else HtmlBuilder

    # адаптер (структурный)
    def build_page(self, obj: HtmlWidget):
        return self.builder.generate_html(obj.sections, obj.divs, inline=obj.inline)
