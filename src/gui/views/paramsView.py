from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QModelIndex
from gui.widgets.parametersTableWidget import ParametersTableModel
from gui.widgets.parametersTableWidget import ParametersTableView
import os
from PyQt5 import uic
import logging
import json
import time

log = logging.getLogger(__name__)

paramsViewUiPath = os.path.dirname(os.path.realpath(__file__)) + '\\paramsViewUi.ui'
Ui_paramsView, QtBaseClass = uic.loadUiType(paramsViewUiPath)


class ParametersView(QWidget, Ui_paramsView):  # type: QWidget

    def __init__(self, model=None, controller=None):
        super(ParametersView, self).__init__()
        self.setupUi(self)
        self.model = model
        self.setup_table()
        with open(self.model.defaultFilePath, 'r') as fp:
            dictParameters = json.load(fp)
            self.temporaryParametersDict = dictParameters[0]

    def setup_table(self):
        self.tableModel = ParametersTableModel()
        self.tableView = ParametersTableView(self, self.tableModel)
        self.tableView.setObjectName("parametersTableView")
        self.tableWidgetLayout = QVBoxLayout()
        self.tableWidgetLayout.addWidget(self.tableView.table_view)
        self.tableWidget.setLayout(self.tableWidgetLayout)
        self.tableView.load_json(self.model.defaultFilePath)
        self.pb_save.clicked.connect(self.save_parameters)
        self.tableModel.dataChanged.connect(self.update_temporary_dict)

    def udpate_graph(self):
        pass

    @pyqtSlot(QModelIndex)
    def update_temporary_dict(self, value):
        ageGroup = self.tableModel.data[value.row()][0]
        try:
            parametersName = self.tableModel.data[value.row()][1]
            parametersValue1 = self.tableModel.data[value.row()][2]
            parametersValue2 = self.tableModel.data[value.row()][3]
            self.temporaryParametersDict[ageGroup][parametersName]['p1'] = parametersValue1
            self.temporaryParametersDict[ageGroup][parametersName]['p2'] = parametersValue2
        except KeyError:
            msgBox = QMessageBox()
            msgBox.setText('Age group is undefined')
            msgBox.exec_()

    def save_parameters(self):
        defaultSimulationParametersJsonFilename = time.strftime("simulationParameters_%Y-%m-%d_%Hh%Mm%Ss.json")
        try:
            simulationParametersFilename, _ = \
                QFileDialog.getSaveFileName(directory=defaultSimulationParametersJsonFilename)
            with open(simulationParametersFilename, 'w') as fp:
                json.dump(self.temporaryParametersDict, fp)
        except Exception as E:
            log.error(E)