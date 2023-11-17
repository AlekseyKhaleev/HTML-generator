from sys import argv

from PySide6.QtWidgets import QApplication

from source.app import MainApp


def main():
    app = QApplication(argv)
    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
