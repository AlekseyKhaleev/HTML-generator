class HtmlBuilder:
    """
    Класс, представляющий HTML тег.

    Attributes:
        __level (int): Уровень тега.
        __accumulated_tags (str): Накопленные теги.

    Methods:
        __init__(self, tag, *, inline = False):
            Инициализирует новый экземпляр класса.

        __enter__(self) -> 'HtmlTag':
            Входит в контекст тега.

        __exit__(self, exc_type, exc_value, traceback) -> None:
            Выходит из контекста тега.

        fill(self, text: str) -> None:
            Заполняет тег текстом.

        generate_html(cls, sections: int = 0, tags: int = 0, *, inline: bool = False) -> str:
            Генерирует HTML на основе указанных разделов и тегов.
    """
    __level = -1
    __accumulated_tags = ""

    def __init__(self, tag, *, inline=False):
        self.tag = tag
        self.inline = inline

    def __enter__(self):
        self.__class__.__level += 1
        type(self).__accumulated_tags += f"{'    ' * self.__level}<{self.tag}>" + ['\n', ''][self.inline]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        type(self).__accumulated_tags += f"{['    ' * self.__class__.__level, ''][self.inline]}</{self.tag}>\n"
        self.__class__.__level -= 1

    def fill(self, text):
        type(self).__accumulated_tags += ['    ' * (self.__class__.__level + 1), ''][self.inline] + text + ['\n', ''][
            self.inline]

    @classmethod
    def generate_html(cls, sections=0, tags=0, *, inline=False):
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
