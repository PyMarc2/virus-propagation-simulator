"""
QDialogBox GUI for login-in using an Rekognition AI hosted the developper's private AWS server.

TODO: Add the possibility to add a face to the dataBank in a new dialog.
TODO: Add the SAP formatting of data
TODO: Test all SAP connections with database
TODO: make a general logger in the software


Author:
        Marc-André Vigneault <marc-andre.vigneault@ca.abb.com> ULaval
        Paul Bareil <paul.bareil@ca.abb.com> ABB Bomem Qc

Change Log
Date: Semaine 22 Juillet, 2019 :    - First Draft + FrontEnd begining
Date: Semaine 29 Juillet, 2019 :    - Improvements backend + Threading login AI + Improvements GUI
Date: Semaine 12 Aout, 2019         - Improvement on connection (proxies). Threads for connection lookout, More fluid and quick.
Date: Semaine 19 Aout, 2019         - BackEnd SAP begining + réglage de bugs.
"""

__author__ = "Marc-André Vigneault", "Paul Bareil"
__copyright__ = "Copyright 2019, ABB"
__credits__ = ["Marc-André Vigneault", "Paul Bareil"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Marc-André Vigneault", "Paul Bareil"
__email__ = "marc-andre.vigneault@ca.abb.com"
__status__ = "Production"

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QPainter, QMovie, QIcon
from views.mainWindow import MainWindow
from models.mainModel import MainModel
from models.mainController import MainController
from tools.threadWorker import Worker
from tools.UiCustomizationLib import LoadingDotsWidget, LoadingDotsSplash
import sys
import time
import ctypes
import threading
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os

log = logging.getLogger(__name__)

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setStyle("Fusion")
        self.setStyleSheet('''
    
    font:75 12pt "Helvetica";
    
    
    QWidget {
    background-color: #EFF6EE;
    color: #191712;
    font:75 10pt "ABBvoice";
    border-color: #ff0011;
}

QHeaderView::section {
    background-color: #233043;
    color: #EFF6EE;
    padding: 4px;
    border: 1px solid #fffff8;
    font-size: 14pt;
    font: 75 10pt "ABBvoice";
}

QTableWidget {
    gridline-color: #fffff8;
    font-size: 12pt;
}

QTableWidget QTableCornerButton::section {
    background-color: #646464;
    border: 1px solid #fffff8;
}

''')
        self.setStyleSheet("")
        sys.excepthook = self.handle_exception
        self.splash()
        self.mainView.setWindowTitle("SAP-FormLink")
        self.mainView.show()

    def splash(self):
        pixmap = QPixmap(".\\images\\ABB_logo.png")
        smallerPixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        splash = QSplashScreen(smallerPixmap, Qt.WindowStaysOnTopHint)
        splash.setMask(smallerPixmap.mask())
        splash.setWindowFlag(Qt.WindowStaysOnTopHint)
        splash.show()
        self.processEvents()
        self.init_logging()
        self.processEvents()
        log.info("Initialization of views, models, controllers...")
        self.processEvents()
        self.mainModel = MainModel()
        self.mainCtrl = MainController(self.mainModel)
        self.mainView = MainWindow(self.mainModel, self.mainCtrl)
        self.mainView.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.processEvents()
        log.info("Initialization completed.")
        self.processEvents()

    @staticmethod
    def init_logging():
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)

        # create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter(
            "%(asctime)s\t\t (%(name)-15.15s) (thread:%(thread)d) (line:%(lineno)5d)\t\t[%(levelname)-5.5s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # create debug file handler in working directory
        handler = RotatingFileHandler(os.path.join(
            os.getcwd(), "SAP-FormLink.log"), maxBytes=2.3 * 1024 * 1024, backupCount=5)
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter(
            "%(asctime)s\t\t (%(name)-25.25s) (thread:%(thread)d) (line:%(lineno)5d)\t\t[%(levelname)-5.5s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @staticmethod
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        log.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def main():
    # Makes the icon in the taskbar as well.
    appID = 'ABB.SAP-formLink.version0.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)

    app = App(sys.argv)
    app.setWindowIcon(QIcon(".\\images\\ABB_icon.png"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
