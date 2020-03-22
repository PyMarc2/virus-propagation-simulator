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
        self.connect_signals()
        self.plotItem = self.graphWidget.getPlotItem()

    def connect_buttons(self):
        self.pb_simulate.clicked.connect(self.launch_simulation)
        log.info("Connecting simulationView GUI...")

    def connect_signals(self):
        log.info("Connecting simulationView Signals...")
        self.model.simulatorObject.s_data_changed.connect(self.graph_update)

    @pyqtSlot(list)
    def graph_update(self, value):
        self.plotItem.clear()
        #unfoldedData = self.unfold_plot_data(value)
        #log.info("Plot updated")
        self.plotItem.plot(value[0], value[1][0])



    def unfold_plot_data(self, foldedData):
        unfoldedData = []
        xdata = foldedData[0]
        for ydata in foldedData[1]:
            unfoldedData.append([xdata, ydata])
        return unfoldedData


    def load_simulation_parameters(self):
        pass

    def update_plot(self):
        pass

    def initialize_simulation(self):
        pass

    def launch_simulation(self):
        args = [self.model.populationSize, self.model.initialInfected, self.model.simulationTime]
        log.info("Population Size:{}".format(self.model.populationSize))
        log.info("Population: {}".format(self.model.simulatorObject.population))
        log.info("Parameters: {}".format(self.model.simulatorObject.parameters))
        log.info("Initially Infected: {}".format(self.model.initialInfected))
        self.simulationWorker = Worker(self.model.simulatorObject.simulate_from_gui, *args)
        self.simulationThread = QThread()
        self.simulationWorker.moveToThread(self.simulationThread)
        self.simulationThread.started.connect(self.simulationWorker.run)
        self.simulationThread.start()
