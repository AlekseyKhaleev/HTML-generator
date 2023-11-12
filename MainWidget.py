import os
from fnmatch import fnmatch
from sys import argv
from enum import IntEnum

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QInputDialog, QMainWindow, QStackedLayout, QTextEdit
from PySide6.QtWebEngineWidgets import QWebEngineView

from ui_gen import Ui_MainWindow
from utils import HtmlBuildStrategy, HtmlWidget


class MainApp(QMainWindow, Ui_MainWindow, HtmlWidget):
    __metaclass__ = QMainWindow
    saved = Signal()
    __tmp_html_name = "TEMP.html"

    class Mode(IntEnum):
        TEXT = 0
        HTML = 1

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = str()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.update_templates()
        self.text_edit = QTextEdit()
        self.render = QWebEngineView()
        self.text_lay = QStackedLayout()
        self.text_lay.setStackingMode(QStackedLayout.StackOne)
        self.text_lay.addWidget(self.text_edit)
        self.text_lay.addWidget(self.render)
        self.text_view.setLayout(self.text_lay)

        # ---------------------------- connections----------------------------------------
        self.text_btn.clicked.connect(self.show_text)
        self.render_btn.clicked.connect(self.show_html)
        self.generate_btn.clicked.connect(self.generate)
        self.clear_btn.clicked.connect(self.text_edit.clear)
        self.save_btn.clicked.connect(self.save_modal)
        self.saved.connect(self.update_templates)
        self.load_btn.clicked.connect(self.load_template)
        # ---------------------------------------------------------------------------------

    @property
    def sections(self):
        return self.sections_spin.value()

    @property
    def divs(self):
        return self.divs_spin.value()

    @property
    def inline(self):
        return self.inline_check.isChecked()

    def generate(self):
        self.text_edit.clear()
        build_strategy = HtmlBuildStrategy(bordered=self.border_check.isChecked())
        self.data = build_strategy.build_page(self)
        self.text_edit.setPlainText(self.data)
        self.show_text()

    def show_text(self):
        self.text_lay.setCurrentIndex(self.Mode.TEXT)

    def show_html(self):
        self.render.setHtml(self.text_edit.toPlainText())
        self.text_lay.setCurrentIndex(self.Mode.HTML)

    def save_modal(self):
        modal = QInputDialog()
        modal.setWindowTitle("HTML template saving")
        modal.setLabelText("Enter filename:")
        modal.exec()
        if modal.accepted:
            self.save_template(modal.textValue())

    def save_template(self, filename):
        with open(f"templates/{filename.rstrip('.html')}.html", "w") as output:
            output.write(self.data)
        self.saved.emit()

    def update_templates(self):
        self.templates.clear()
        self.templates.addItems(self.get_templates())

    @staticmethod
    def get_templates():
        return tuple(entry for entry in os.listdir("templates") if fnmatch(entry, "*.html"))

    def load_template(self):
        path = str(self.templates.currentText())
        with open(f"templates/{path}", "r") as temp:
            self.data = temp.read()
            self.text_edit.setPlainText(self.data)
            self.show_text()


def main():
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
