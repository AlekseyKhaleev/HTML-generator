import os
from enum import IntEnum
from fnmatch import fnmatch


from PySide6.QtCore import Signal, QCoreApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QInputDialog, QMainWindow, QStackedLayout, QTextEdit


from designed_ui.designed_interface import Ui_MainWindow
from source.utils import HtmlAdapter, HtmlWidget


class MainWindow(QMainWindow, Ui_MainWindow, HtmlWidget):
    temp_saved = Signal()
    temp_loaded = Signal()
    temp_generated = Signal()

    class Mode(IntEnum):
        TEXT = 0
        HTML = 1

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.update_templates()
        self.text_edit = QTextEdit()
        self.html_render = QWebEngineView()
        self.html_render.reload()
        self.text_lay = QStackedLayout()
        self.text_lay.setStackingMode(QStackedLayout.StackOne)
        self.text_lay.addWidget(self.text_edit)
        self.text_lay.addWidget(self.html_render)
        self.text_view.setLayout(self.text_lay)
        # ---------------------------- connections----------------------------------------
        self.text_btn.clicked.connect(self.show_text)
        self.render_btn.clicked.connect(self.show_html)
        self.generate_btn.clicked.connect(self.generate)
        self.clear_btn.clicked.connect(self.text_edit.clear)
        self.save_btn.clicked.connect(self.save_modal)
        self.load_btn.clicked.connect(self.load_template)
        self.temp_saved.connect(self.update_templates)
        self.temp_loaded.connect(self.show_text)
        self.temp_generated.connect(self.show_text)
        # ---------------------------------------------------------------------------------

    @property
    def sections(self) -> int:
        return self.sections_spin.value()

    @property
    def divs(self) -> int:
        return self.divs_spin.value()

    @property
    def inline(self) -> bool:
        return self.inline_check.isChecked()

    def generate(self) -> None:
        html_agent = HtmlAdapter(bordered=self.bordered_check.isChecked())
        html_agent.build_page(self)
        html_text = html_agent.get_html()
        self.text_edit.setPlainText(html_text)
        self.temp_generated.emit()

    def show_text(self) -> None:
        self.text_lay.setCurrentIndex(self.Mode.TEXT)

    def show_html(self) -> None:
        self.html_render.setHtml(self.text_edit.toPlainText())
        self.text_lay.setCurrentIndex(self.Mode.HTML)

    def save_modal(self) -> None:
        modal = QInputDialog()
        modal.setWindowTitle("HTML template saving")
        modal.setLabelText("Enter filename:")
        modal.exec()
        if modal.accepted:
            self.save_template(modal.textValue())

    def save_template(self, filename) -> None:
        with open(f"templates/{filename.rstrip('.html')}.html", "w") as output:
            output.write(self.text_edit.toPlainText())
        self.temp_saved.emit()

    def update_templates(self) -> None:
        self.templates.clear()
        self.templates.addItems(self.get_templates())

    @staticmethod
    def get_templates() -> tuple[str, ...]:
        return tuple(entry for entry in os.listdir("templates") if fnmatch(entry, "*.html"))

    def load_template(self) -> None:
        template_name = str(self.templates.currentText())
        with open(f"templates/{template_name}", "r") as temp:
            template_text = temp.read()
            self.text_edit.setPlainText(template_text)
            self.temp_loaded.emit()
