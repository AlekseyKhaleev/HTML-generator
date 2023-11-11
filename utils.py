from functools import wraps, update_wrapper
from abc import ABC, abstractmethod


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
    __level = -1
    __accumulated_tags = ""

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
        type(self).__level += 1
        type(self).__accumulated_tags += f"{'    ' * type(self).__level}<{self._tag}>" + ['\n', ''][self._inline]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Выходит из контекстного менеджера, закрывая HTML-тег.

        Args:
            exc_type: Тип исключения.
            exc_value: Значение исключения.
            traceback: Отслеживание исключения.
        """
        type(self).__accumulated_tags += f"{['    ' * type(self).__level, ''][self._inline]}</{self._tag}>\n"
        type(self).__level -= 1

    def fill(self, text):
        """
        Заполняет HTML-элемент данным текстом.

        Args:
            text (str): Текст для заполнения HTML-элемента.
        """
        type(self).__accumulated_tags += ['    ' * (type(self).__level + 1), ''][self._inline] + text + ['\n', ''][
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
        cls = border_divs(cls)

        cls.__accumulated_tags += "<!DOCTYPE html>\n"
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
        result, cls.__accumulated_tags = cls.__accumulated_tags, ""
        return result


def border_divs(cls: type[HtmlBuilder]) -> type[HtmlBuilder]:
    old_enter = cls.__enter__
    old_exit = cls.__exit__

    @wraps(old_enter)
    def enter_wrapper(self):
        match self._tag:
            case 'head':
                res = old_enter(self)
                with cls('style') as style:
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

    cls.__enter__ = enter_wrapper
    cls.__exit__ = exit_wrapper
    return cls


class HtmlBuildStrategy(ABC):
    __accumulated_tags = ""

    @abstractmethod
    def generate_html(self, sections=0, tags=0, *, inline=False):
        pass


class SimpleBuild(HtmlBuildStrategy):
    def generate_html(self, sections=0, tags=0, *, inline=False):
        return HtmlBuilder.generate_html(sections, tags, inline=inline)


class BorderedBuild(HtmlBuildStrategy):
    def generate_html(self, sections=0, tags=0, *, inline=False):
        return HtmlBuilder.generate_html(sections, tags, inline=inline)
