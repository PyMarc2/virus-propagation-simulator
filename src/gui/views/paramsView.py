from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from gui.widgets.parametersTableWidget import ParametersTableModel
from gui.widgets.parametersTableWidget import ParametersTableView
import os
from PyQt5 import uic
import logging

log = logging.getLogger(__name__)

paramsViewUiPath = os.path.dirname(os.path.realpath(__file__)) + '\\paramsViewUi.ui'
Ui_paramsView, QtBaseClass = uic.loadUiType(paramsViewUiPath)


class ParametersView(QWidget, Ui_paramsView): #type: QWidget

    def __init__(self, model=None, controller=None):
        super(ParametersView, self).__init__()
        self.setupUi(self)
        self.model = model
        self.setup_table()
        self.temporaryParametersJson = None

    def setup_table(self):
        self.tableModel = ParametersTableModel()
        self.tableView = ParametersTableView(self, self.tableModel)
        self.tableView.setObjectName("parametersTableView")
        self.tableWidgetLayout = QVBoxLayout()
        self.tableWidgetLayout.addWidget(self.tableView.table_view)
        self.tableWidget.setLayout(self.tableWidgetLayout)
        self.tableView.load_json(self.model.defaultFilePath)

    def udpate_graph(self):
        pass

    def save_parameters(self):
        pass



