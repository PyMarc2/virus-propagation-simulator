__author__ = "Marc-André Vigneault"
__copyright__ = "Copyright 2019, Marc-André Vigneault"
__credits__ = ["Marc-André Vigneault"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Marc-André Vigneault"
__email__ = "marc-andre.vigneault@ulaval.ca"
__status__ = "Production"

from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QPainter, QMovie, QIcon
from gui.windows.mainWindow import MainWindow
from mainModel import MainModel
from VirusSimulator import VirusSimulator
from tools.threadWorker import Worker
import sys
import ctypes
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os

log = logging.getLogger(__name__)


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        sys.excepthook = self.handle_exception
        self.init_logging()

        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setStyle("Fusion")
        self.setStyleSheet("")

        self.mainModel = MainModel()
        simulator = VirusSimulator()
        self.mainModel.simulatorObject = simulator
        self.mainWindow = MainWindow(model = self.mainModel)
        self.mainWindow.setWindowTitle("py-virus-propagation-simulator")
        self.mainWindow.show()

    @staticmethod
    def init_logging():
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)

        # create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter("%(asctime)s\t\t (%(name)-15.15s) (thread:%(thread)d) (line:%(lineno)5d)\t\t[%(levelname)-5.5s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # create debug file handler in working directory
        handler = RotatingFileHandler(os.path.join(os.getcwd(), "SAP-FormLink.log"), maxBytes=2.3 * 1024 * 1024, backupCount=5)
        handler.setLevel(logging.NOTSET)
        formatter = logging.Formatter("%(asctime)s\t\t (%(name)-25.25s) (thread:%(thread)d) (line:%(lineno)5d)\t\t[%(levelname)-5.5s] %(message)s")
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
    appID = 'py-virus-propagation-simulator'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appID)
    app = App(sys.argv)
    app.setWindowIcon(QIcon("\\img\\biohazzard.png"))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()