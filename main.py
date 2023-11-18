import ctypes
from sys import argv

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from source.app import MainWindow


def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('NNSTU.html_generator.1')
    app = QApplication(argv)
    window = MainWindow()
    window.setWindowIcon(QIcon("designed_ui/icons/logo.png"))
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
