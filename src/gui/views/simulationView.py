from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread
from tools.threadWorker import Worker
import os
from PyQt5 import uic
import logging

log = logging.getLogger(__name__)


simulationViewUiPath = os.path.dirname(os.path.realpath(__file__)) + '\\simulationViewUi.ui'
Ui_simulationView, QtBaseClass = uic.loadUiType(simulationViewUiPath)


class SimulationView(QWidget, Ui_simulationView):

    def __init__(self, model=None, controller=None):
        super(SimulationView, self).__init__()
        self.model = model
        self.setupUi(self)
        self.connect_buttons()

    def connect_buttons(self):
        self.pb_simulate.clicked.connect(self.launch_simulation)

    def load_simulation_parameters(self):
        pass

    def update_plot(self):
        pass

    def initialize_simulation(self):
        pass

    def launch_simulation(self):
        self.simulationWorker = Worker(self.model.simulatorObject.simulate)
        self.simulationThread = QThread()
        self.simulationWorker.moveToThread(self.simulationThread)
        self.simulationThread.started.connect(self.simulationWorker.run)
        self.simulationThread.start()



