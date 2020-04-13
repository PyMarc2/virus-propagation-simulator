from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QModelIndex, Qt, QAbstractItemModel
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
        self.selected_item_index = None
        with open(self.model.defaultFilePath, 'r') as fp:
            dictParameters = json.load(fp)
            self.temporaryParametersDict = dictParameters[0]
        self.setup_table()

    def setup_table(self):
        self.tableModel = ParametersTableModel()
        self.tableView = ParametersTableView(self, self.tableModel)
        self.tableView.setObjectName("parametersTableView")
        self.tableWidgetLayout = QVBoxLayout()
        self.tableWidgetLayout.addWidget(self.tableView.table_view)
        self.tableWidget.setLayout(self.tableWidgetLayout)
        self.tableView.load_data(self.temporaryParametersDict)
        for i in range(0, self.tableModel.rowCount()):
            self.tableView.table_view.openPersistentEditor(self.tableModel.index(i, 0))
        self.pb_save.clicked.connect(self.save_parameters)
        self.tableModel.dataChanged.connect(self.update_data)
        self.rb_binomial.clicked.connect(self.update_distribution_type_in_dict)
        self.rb_normal.clicked.connect(self.update_distribution_type_in_dict)
        self.rb_gamma.clicked.connect(self.update_distribution_type_in_dict)

    def udpate_graph(self):
        pass

    @pyqtSlot(QModelIndex)
    def update_data(self, index):
        try:
            if index.column() == 0:
                self.update_data_from_dict(index)
            else:
                self.update_dict_from_data(index)
        except Exception as E:
            log.error(E)

    def update_data_from_dict(self, index):
        ageGroup = self.tableModel.data[index.row()][0]
        parametersName = self.tableModel.data[index.row()][1]
        parametersindex1 = self.temporaryParametersDict[ageGroup][parametersName]['p1']
        parametersindex2 = self.temporaryParametersDict[ageGroup][parametersName]['p2']
        self.tableModel.setData(index.sibling(index.row(), 2), parametersindex1, Qt.EditRole)
        self.tableModel.setData(index.sibling(index.row(), 3), parametersindex2, Qt.EditRole)

    def update_dict_from_data(self, index):
        ageGroup = self.tableModel.data[index.row()][0]
        parametersName = self.tableModel.data[index.row()][1]
        parametersindex1 = self.tableModel.data[index.row()][2]
        parametersindex2 = self.tableModel.data[index.row()][3]
        self.temporaryParametersDict[ageGroup][parametersName]['p1'] = parametersindex1
        self.temporaryParametersDict[ageGroup][parametersName]['p2'] = parametersindex2

    def update_distribution_type_in_dict(self):
        try:
            ageGroup = self.tableModel.data[self.selected_item_index.row()][0]
            parameter = self.tableModel.data[self.selected_item_index.row()][1]
            if self.rb_binomial.isChecked():
                self.temporaryParametersDict[ageGroup][parameter]['distributionType'] = self.rb_binomial.text()
            elif self.rb_normal.isChecked():
                self.temporaryParametersDict[ageGroup][parameter]['distributionType'] = self.rb_normal.text()
            elif self.rb_gamma.isChecked():
                self.temporaryParametersDict[ageGroup][parameter]['distributionType'] = self.rb_gamma.text()
        except Exception as E:
            log.error(E)

    def set_radio_button_value(self):
        try:
            ageGroup = self.tableModel.data[self.selected_item_index.row()][0]
            parameter = self.tableModel.data[self.selected_item_index.row()][1]
            distributionType = self.temporaryParametersDict[ageGroup][parameter]['distributionType']
            if distributionType == 'Normal':
                self.rb_normal.setChecked(True)
            elif distributionType == 'Binomial':
                self.rb_binomial.setChecked(True)
            elif distributionType == 'Gamma':
                self.rb_gamma.setChecked(True)
        except Exception as E:
            log.error(E)

    def save_parameters(self):
        defaultSimulationParametersJsonFilename = time.strftime("simulationParameters_%Y-%m-%d_%Hh%Mm%Ss.json")
        try:
            simulationParametersFilename, _ = \
                QFileDialog.getSaveFileName(directory=defaultSimulationParametersJsonFilename)
            with open(simulationParametersFilename, 'w') as fp:
                json.dump(self.temporaryParametersDict, fp)
        except Exception as E:
            log.error(E)