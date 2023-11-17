# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designed_interface.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpinBox,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(877, 682)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.templates = QComboBox(self.centralwidget)
        self.templates.addItem("")
        self.templates.addItem("")
        self.templates.setObjectName(u"templates")
        self.templates.setGeometry(QRect(580, 90, 261, 31))
        self.templates.setEditable(False)
        self.sections_spin = QSpinBox(self.centralwidget)
        self.sections_spin.setObjectName(u"sections_spin")
        self.sections_spin.setGeometry(QRect(580, 230, 121, 22))
        self.sections_label = QLabel(self.centralwidget)
        self.sections_label.setObjectName(u"sections_label")
        self.sections_label.setGeometry(QRect(580, 200, 71, 21))
        self.divs_spin = QSpinBox(self.centralwidget)
        self.divs_spin.setObjectName(u"divs_spin")
        self.divs_spin.setGeometry(QRect(720, 230, 121, 22))
        self.divs_label = QLabel(self.centralwidget)
        self.divs_label.setObjectName(u"divs_label")
        self.divs_label.setGeometry(QRect(720, 200, 121, 21))
        self.generate_btn = QPushButton(self.centralwidget)
        self.generate_btn.setObjectName(u"generate_btn")
        self.generate_btn.setGeometry(QRect(660, 520, 111, 41))
        self.text_btn = QPushButton(self.centralwidget)
        self.text_btn.setObjectName(u"text_btn")
        self.text_btn.setGeometry(QRect(20, 20, 75, 24))
        self.render_btn = QPushButton(self.centralwidget)
        self.render_btn.setObjectName(u"render_btn")
        self.render_btn.setGeometry(QRect(90, 20, 75, 24))
        self.save_btn = QPushButton(self.centralwidget)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setGeometry(QRect(760, 590, 75, 24))
        self.template_label = QLabel(self.centralwidget)
        self.template_label.setObjectName(u"template_label")
        self.template_label.setGeometry(QRect(580, 60, 81, 21))
        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName(u"clear_btn")
        self.clear_btn.setGeometry(QRect(590, 590, 81, 24))
        self.inline_check = QCheckBox(self.centralwidget)
        self.inline_check.setObjectName(u"inline_check")
        self.inline_check.setGeometry(QRect(580, 300, 91, 20))
        self.load_btn = QPushButton(self.centralwidget)
        self.load_btn.setObjectName(u"load_btn")
        self.load_btn.setGeometry(QRect(750, 130, 91, 31))
        self.divs_settings_label = QLabel(self.centralwidget)
        self.divs_settings_label.setObjectName(u"divs_settings_label")
        self.divs_settings_label.setGeometry(QRect(670, 270, 141, 31))
        self.bordered_check = QCheckBox(self.centralwidget)
        self.bordered_check.setObjectName(u"bordered_check")
        self.bordered_check.setGeometry(QRect(580, 330, 91, 20))
        self.alignment_spin = QComboBox(self.centralwidget)
        self.alignment_spin.addItem("")
        self.alignment_spin.addItem("")
        self.alignment_spin.addItem("")
        self.alignment_spin.setObjectName(u"alignment_spin")
        self.alignment_spin.setGeometry(QRect(580, 400, 261, 22))
        self.alignment_spin.setEditable(False)
        self.alignment_label = QLabel(self.centralwidget)
        self.alignment_label.setObjectName(u"alignment_label")
        self.alignment_label.setGeometry(QRect(580, 370, 81, 21))
        self.text_color_spin = QComboBox(self.centralwidget)
        self.text_color_spin.addItem("")
        self.text_color_spin.addItem("")
        self.text_color_spin.addItem("")
        self.text_color_spin.addItem("")
        self.text_color_spin.addItem("")
        self.text_color_spin.setObjectName(u"text_color_spin")
        self.text_color_spin.setGeometry(QRect(580, 480, 261, 22))
        self.text_color_spin.setEditable(False)
        self.text_color_label = QLabel(self.centralwidget)
        self.text_color_label.setObjectName(u"text_color_label")
        self.text_color_label.setGeometry(QRect(580, 450, 81, 16))
        self.text_view = QWidget(self.centralwidget)
        self.text_view.setObjectName(u"text_view")
        self.text_view.setGeometry(QRect(20, 60, 531, 581))
        self.headers_check = QCheckBox(self.centralwidget)
        self.headers_check.setObjectName(u"headers_check")
        self.headers_check.setGeometry(QRect(730, 330, 111, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.templates.setItemText(0, QCoreApplication.translate("MainWindow", u"Empty", None))
        self.templates.setItemText(1, QCoreApplication.translate("MainWindow", u"Standard", None))

        self.sections_label.setText(QCoreApplication.translate("MainWindow", u"Sections", None))
        self.divs_label.setText(QCoreApplication.translate("MainWindow", u"Divs per section", None))
        self.generate_btn.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.text_btn.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        self.render_btn.setText(QCoreApplication.translate("MainWindow", u"Render", None))
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.template_label.setText(QCoreApplication.translate("MainWindow", u"Template", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.inline_check.setText(QCoreApplication.translate("MainWindow", u"inline", None))
        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.divs_settings_label.setText(QCoreApplication.translate("MainWindow", u"Divs settings:", None))
        self.bordered_check.setText(QCoreApplication.translate("MainWindow", u"bordered", None))
        self.alignment_spin.setItemText(0, QCoreApplication.translate("MainWindow", u"Left", None))
        self.alignment_spin.setItemText(1, QCoreApplication.translate("MainWindow", u"Center", None))
        self.alignment_spin.setItemText(2, QCoreApplication.translate("MainWindow", u"Right", None))

        self.alignment_label.setText(QCoreApplication.translate("MainWindow", u"Alignment", None))
        self.text_color_spin.setItemText(0, QCoreApplication.translate("MainWindow", u"Black", None))
        self.text_color_spin.setItemText(1, QCoreApplication.translate("MainWindow", u"Red", None))
        self.text_color_spin.setItemText(2, QCoreApplication.translate("MainWindow", u"Green", None))
        self.text_color_spin.setItemText(3, QCoreApplication.translate("MainWindow", u"Yellow", None))
        self.text_color_spin.setItemText(4, QCoreApplication.translate("MainWindow", u"Blue", None))

        self.text_color_label.setText(QCoreApplication.translate("MainWindow", u"Text color:", None))
        self.headers_check.setText(QCoreApplication.translate("MainWindow", u"with headers", None))
    # retranslateUi

