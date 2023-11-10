class HtmlTag:
    level = -1
    page = "<!DOCTYPE html>\n"

    def __init__(self, tag, *, inline=False, new=False):
        self.tag = tag
        self.inline = inline
        if new:
            self.__class__.page = "<!DOCTYPE html>\n"

    def __enter__(self):
        self.__class__.level += 1
        type(self).page += f"{'    ' * self.level}<{self.tag}>" + ['\n', ''][self.inline]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        type(self).page += f"{['    ' * self.__class__.level, ''][self.inline]}</{self.tag}>\n"
        self.__class__.level -= 1

    def fill(self, text):
        type(self).page += ['    ' * (self.__class__.level + 1), ''][self.inline] + text + ['\n', ''][self.inline]

    @classmethod
    def generate_html(cls, sections=0, tags=0, *, inline=False):
        with cls('html', new=True):
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

        return cls.page



