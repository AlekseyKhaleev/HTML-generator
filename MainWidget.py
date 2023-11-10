from fnmatch import fnmatch
from os import listdir
from sys import argv

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QInputDialog, QMainWindow


from ui_gen import Ui_MainWindow
from utils import generate_html


class MainApp(QMainWindow, Ui_MainWindow):
    saved = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = ""
        self.update_templates()

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
        self.data = generate_html(self.sections_spin.value(), self.divs_spin.value(),
                                  inline=self.inline_check.isChecked())
        self.set_text()

    def set_text(self):
        self.text_edit.setPlainText(self.data)

    def set_html(self):
        self.data = self.text_edit.toPlainText()
        self.text_edit.setHtml(self.data)

    def save_modal(self):
        modal = QInputDialog()
        modal.setWindowTitle("HTML template saving")
        modal.setLabelText("Enter filename:")
        modal.exec()
        if modal.accepted:
            self.save_template(modal.textValue())

    def save_template(self, filename):
        with open(f"templates/{filename}.html", "w") as output:
            output.write(self.data)
        self.saved.emit()


    def update_templates(self):
        self.templates.clear()
        self.templates.addItems(self.get_templates())

    @staticmethod
    def get_templates():
        return tuple(entry for entry in listdir("templates") if fnmatch(entry, "*.html"))

    def load_template(self):
        path = str(self.templates.currentText())
        with open(f"templates/{path}", "r") as temp:
            self.data = temp.read()
            self.set_text()



def main():
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
