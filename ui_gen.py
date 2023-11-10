# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'html.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpinBox, QStatusBar, QTextEdit, QTreeView,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(881, 663)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.templates = QComboBox(self.centralwidget)
        self.templates.setObjectName(u"templates")
        self.templates.setGeometry(QRect(590, 90, 241, 22))
        self.templates.setEditable(False)
        self.sections_spin = QSpinBox(self.centralwidget)
        self.sections_spin.setObjectName(u"sections_spin")
        self.sections_spin.setGeometry(QRect(590, 170, 131, 22))
        self.sections_label = QLabel(self.centralwidget)
        self.sections_label.setObjectName(u"sections_label")
        self.sections_label.setGeometry(QRect(590, 150, 49, 16))
        self.divs_spin = QSpinBox(self.centralwidget)
        self.divs_spin.setObjectName(u"divs_spin")
        self.divs_spin.setGeometry(QRect(590, 230, 131, 22))
        self.divs_label = QLabel(self.centralwidget)
        self.divs_label.setObjectName(u"divs_label")
        self.divs_label.setGeometry(QRect(590, 210, 131, 16))
        self.generate_btn = QPushButton(self.centralwidget)
        self.generate_btn.setObjectName(u"generate_btn")
        self.generate_btn.setGeometry(QRect(590, 270, 75, 24))
        self.text_btn = QPushButton(self.centralwidget)
        self.text_btn.setObjectName(u"text_btn")
        self.text_btn.setGeometry(QRect(40, 20, 75, 24))
        self.render_btn = QPushButton(self.centralwidget)
        self.render_btn.setObjectName(u"render_btn")
        self.render_btn.setGeometry(QRect(110, 20, 75, 24))
        self.save_btn = QPushButton(self.centralwidget)
        self.save_btn.setObjectName(u"save_btn")
        self.save_btn.setGeometry(QRect(760, 270, 71, 24))
        self.text_edit = QTextEdit(self.centralwidget)
        self.text_edit.setObjectName(u"text_edit")
        self.text_edit.setGeometry(QRect(30, 60, 521, 571))
        self.text_edit.setFocusPolicy(Qt.ClickFocus)
        self.text_edit.setAcceptDrops(False)
        self.text_edit.setTabChangesFocus(False)
        self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
        self.template_label = QLabel(self.centralwidget)
        self.template_label.setObjectName(u"template_label")
        self.template_label.setGeometry(QRect(590, 70, 49, 16))
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setGeometry(QRect(580, 370, 251, 261))
        self.current_section_combo = QComboBox(self.centralwidget)
        self.current_section_combo.setObjectName(u"current_section_combo")
        self.current_section_combo.setGeometry(QRect(580, 340, 251, 22))
        self.current_section_combo.setEditable(False)
        self.inline_check = QCheckBox(self.centralwidget)
        self.inline_check.setObjectName(u"inline_check")
        self.inline_check.setGeometry(QRect(760, 230, 76, 20))
        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName(u"clear_btn")
        self.clear_btn.setGeometry(QRect(670, 270, 81, 24))
        self.load_btn = QPushButton(self.centralwidget)
        self.load_btn.setObjectName(u"load_btn")
        self.load_btn.setGeometry(QRect(760, 120, 71, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.sections_label.setText(QCoreApplication.translate("MainWindow", u"Sections", None))
        self.divs_label.setText(QCoreApplication.translate("MainWindow", u"Tags per section", None))
        self.generate_btn.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.text_btn.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        self.render_btn.setText(QCoreApplication.translate("MainWindow", u"Render", None))
        self.save_btn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.template_label.setText(QCoreApplication.translate("MainWindow", u"Template", None))
        self.inline_check.setText(QCoreApplication.translate("MainWindow", u"Inline", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.load_btn.setText(QCoreApplication.translate("MainWindow", u"Load", None))
    # retranslateUi

