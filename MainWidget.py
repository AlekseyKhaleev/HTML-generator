import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
import html  # Это наш конвертированный файл дизайна
from enum import IntEnum
from functools import partial


class ExampleApp(QtWidgets.QMainWindow, html.Ui_MainWindow):
    class HtmlView(IntEnum):
        TEXT = 0
        RENDER = 1

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.template_data = {}
        self.text_edit.setText("text")
        self.render_edit.setText("render")
        self.html_browser.setCurrentIndex(self.HtmlView.TEXT)

        # -------------------------- connections----------------------------------------
        self.text_btn.clicked.connect(partial(self.switch_view, self.HtmlView.TEXT))
        self.render_btn.clicked.connect(partial(self.switch_view, self.HtmlView.RENDER))
        self.generate_btn.clicked.connect(self.generate)
        self.sections_btn.clicked.connect(self.set_sections)
        self.divs_btn.clicked.connect(self.set_divs)

    def set_sections(self):
        self.template_data['sections'] = self.sections_spin.value()

    def set_divs(self):
        self.template_data['divs'] = self.divs_spin.value()

    def generate(self):
        self.text_edit.setText(' + '.join(map(str, self.template_data.values())))

    def switch_view(self, page_index):
        self.html_browser.setCurrentIndex(page_index)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
