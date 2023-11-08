import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
import html  # Это наш конвертированный файл дизайна
from enum import IntEnum
from functools import partial
from utils import generate_html


class ExampleApp(QtWidgets.QMainWindow, html.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.template_data = {}
        self.data = ""

        # -------------------------- connections----------------------------------------
        # self.text_btn.clicked.connect(partial(self.switch_view, self.HtmlView.TEXT))
        # self.render_btn.clicked.connect(partial(self.switch_view, self.HtmlView.RENDER))
        self.text_btn.clicked.connect(self.set_text)
        self.render_btn.clicked.connect(self.set_html)
        self.generate_btn.clicked.connect(self.generate)
        self.sections_btn.clicked.connect(self.set_sections)
        self.divs_btn.clicked.connect(self.set_divs)

    def set_sections(self):
        self.template_data['sections'] = self.sections_spin.value()

    def set_divs(self):
        self.template_data['divs'] = self.divs_spin.value()

    def generate(self):
        # self.text_edit.setText(' + '.join(map(str, self.template_data.values())))
        self.text_edit.clear()
        self.data = generate_html()
        self.set_text()

    def set_text(self):
        self.text_edit.setPlainText(self.data)

    def set_html(self):
        self.text_edit.setHtml(self.data)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
