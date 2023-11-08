class HtmlTag:
    level = -1
    page = "<!DOCTYPE html>\n"

    def __init__(self, tag, *, inline=False):
        self.tag = tag
        self.inline = inline

    def __enter__(self):
        self.__class__.level += 1
        type(self).page += f"{'  ' * self.level}<{self.tag}>" + ['\n', ''][self.inline]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        type(self).page += f"{['  ' * self.__class__.level, ''][self.inline]}</{self.tag}>\n"
        self.__class__.level -= 1

    def fill(self, text):
        type(self).page += ['  ' * (self.__class__.level + 1), ''][self.inline] + text + ['\n', ''][self.inline]


if __name__ == '__main__':
    with HtmlTag('html'):
        with HtmlTag('head'):
            pass
        with HtmlTag('body'):
            with HtmlTag('header', inline=True):
                pass
            with HtmlTag('main'):
                with HtmlTag('section'):
                    with HtmlTag('h1', inline=True) as header:
                        header.fill('Первая секция')
                with HtmlTag('section'):
                    with HtmlTag('h1', inline=True) as header:
                        header.fill('Вторая секция')
                    with HtmlTag('a', inline=True) as section:
                        section.fill('https://stepik.org/media/attachments/course/98974/watch_me.mp4')
            with HtmlTag("footer", inline=True):
                pass


    print(HtmlTag.page)
