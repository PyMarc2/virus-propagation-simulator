from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import os
from PyQt5 import uic
import logging

log = logging.getLogger(__name__)

paramsViewUiPath = os.path.dirname(os.path.realpath(__file__)) + '\\paramsViewUi.ui'
Ui_paramsView, QtBaseClass = uic.loadUiType(paramsViewUiPath)


class ParamsView(QWidget, Ui_paramsView):

    def __init__(self, model=None, controller=None):
        super(ParamsView, self).__init__()
        self.setupUi(self)


