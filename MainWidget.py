import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader
import ui_html_gen  # Это наш конвертированный файл дизайна
from utils import generate_html


class MainApp(QtWidgets.QMainWindow, html.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data = ""

        # -------------------------- connections----------------------------------------

        self.text_btn.clicked.connect(self.set_text)
        self.render_btn.clicked.connect(self.set_html)
        self.generate_btn.clicked.connect(self.generate)
        self.clear_btn.clicked.connect(self.text_edit.clear)
        self.save_btn.clicked.connect(self.save_modal)

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
        modal = QtWidgets.QInputDialog()
        modal.setWindowTitle("HTML template saving")
        modal.setLabelText("Enter filename:")
        modal.exec()
        if modal.accepted:
            self.save_template(modal.textValue())

    def save_template(self, filename):
        with open(f"templates/{filename}.html", "w") as output:
            output.write(self.data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
