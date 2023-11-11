import os
from fnmatch import fnmatch
from sys import argv

from PySide6.QtCore import Signal, QUrl
from PySide6.QtWidgets import QApplication, QInputDialog, QMainWindow, QStackedLayout, QTextEdit
from PySide6.QtWebEngineWidgets import QWebEngineView

from ui_gen import Ui_MainWindow
from utils import HtmlBuilder


class MainApp(QMainWindow, Ui_MainWindow):
    saved = Signal()
    __tmp_html_name = "TEMP.html"

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = str()
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.update_templates()
        self.render = QWebEngineView()
        self.text_edit = QTextEdit()
        self.text_lay = QStackedLayout()
        self.text_lay.setStackingMode(QStackedLayout.StackOne)
        self.text_lay.addWidget(self.text_edit)
        self.text_lay.addWidget(self.render)
        self.text_lay.setCurrentIndex(0)
        self.text_view.setLayout(self.text_lay)

        # ---------------------------- connections----------------------------------------
        self.text_btn.clicked.connect(self.set_text)
        self.render_btn.clicked.connect(self.set_html)
        self.generate_btn.clicked.connect(self.generate)
        self.clear_btn.clicked.connect(self.text_edit.clear)
        self.save_btn.clicked.connect(self.save_modal)
        self.saved.connect(self.update_templates)
        self.load_btn.clicked.connect(self.load_template)
        # ---------------------------------------------------------------------------------

    def generate(self):
        self.text_edit.clear()
        self.data = HtmlBuilder.generate_html(self.sections_spin.value(), self.divs_spin.value(),
                                              inline=self.inline_check.isChecked())
        self.text_edit.setPlainText(self.data)
        self.set_text()

    def set_text(self):
        self.text_lay.setCurrentIndex(0)

    def set_html(self):
        self.save_template(type(self).__tmp_html_name)
        print(self.current_dir + f"\\templates\\{type(self).__tmp_html_name}")
        self.render.load(QUrl.fromLocalFile(self.current_dir + f"\\templates\\{type(self).__tmp_html_name}"))
        self.text_lay.setCurrentIndex(1)

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
            self.set_text()


def main():
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
