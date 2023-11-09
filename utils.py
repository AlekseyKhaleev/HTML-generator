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
    def clear(cls):
        cls.page = ""


def generate_html(sections=0, tags=0, *, inline=False):
    with HtmlTag('html', new=True):
        with HtmlTag('head'):
            pass
        with HtmlTag('body'):
            with HtmlTag('header', inline=True):
                pass
            with HtmlTag('main'):
                for sect_num in range(sections):
                    with HtmlTag('section'):
                        for tag_num in range(tags):
                            with HtmlTag('div', inline=inline) as div:
                                div.fill(f"Section {sect_num + 1}, Div {tag_num + 1}")
            with HtmlTag("footer", inline=True):
                pass
    return HtmlTag.page


if __name__ == '__main__':
    print(generate_html())
