from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QMutex
from pyqtgraph import PlotItem
from tools.threadWorker import Worker
from pydispatch import dispatcher
from tools.stoppableThread import QStoppableThread
from Person import Person
import os
from PyQt5 import uic
import logging
import math
import threading

log = logging.getLogger(__name__)

simulationViewUiPath = os.path.dirname(os.path.realpath(__file__)) + '\\simulationViewUi.ui'
Ui_simulationView, QtBaseClass = uic.loadUiType(simulationViewUiPath)

SIGNAL_PLOT_TOGGLED = 'plot.toggled.indicator'

class SimulationView(QWidget, Ui_simulationView):
    SIGNAL_toggled_plot_indicator = 'indicator'

    def __init__(self, model=None, controller=None):
        super(SimulationView, self).__init__()
        self.model = model
        self.allPlotsDict = {}
        self.setupUi(self)
        self.connect_buttons()
        self.connect_signals()
        self.connect_checkbox()
        self.create_plots()
        self.initialize_view()

    def initialize_view(self):
        self.cb_isInfected.setChecked(True)

    def connect_buttons(self):
        self.pb_simulate.clicked.connect(self.launch_simulation)
        log.info("Connecting simulationView GUI...")

    def connect_checkbox(self):
        self.cb_isInfected.stateChanged.connect(lambda: self.toggle_plot("isInfected", caller=self.cb_isInfected))
        self.cb_isInfectious.stateChanged.connect(lambda: self.toggle_plot("isInfectious", caller=self.cb_isInfectious))
        self.cb_isAlive.stateChanged.connect(lambda: self.toggle_plot("isAlive", caller=self.cb_isAlive))
        self.cb_isRecovered.stateChanged.connect(lambda: self.toggle_plot("isRecovered", caller=self.cb_isRecovered))
        self.cb_isHospitalized.stateChanged.connect(
            lambda: self.toggle_plot("isHospitalized", caller=self.cb_isHospitalized))
        self.cb_hasSymptoms.stateChanged.connect(lambda: self.toggle_plot("hasSymptoms", caller=self.cb_hasSymptoms))

    def connect_signals(self):
        log.info("Connecting simulationView Signals...")
        self.model.simulatorObject.s_data_changed.connect(self.update_graph)

    def create_plots(self):
        for indicator in Person().indicators:
            self.allPlotsDict[indicator] = {'plotItem': PlotItem(), 'displayed': 0}
        for indicator in Person().indicators:
            dataPlotItem = self.allPlotsDict[indicator]['plotItem'].plot()
            self.allPlotsDict[indicator]['plotDataItem'] = dataPlotItem
            self.allPlotsDict[indicator]['plotItem'].setTitle(indicator)

    def toggle_plot(self, indicator, caller=None):
        if caller.checkState() == 2:
            self.allPlotsDict[indicator]['displayed'] = 1
            self.update_plots_position()
            dispatcher.send(signal=SIGNAL_PLOT_TOGGLED, sender=self, **{'indicator':indicator})

        elif caller.checkState() == 0:
            self.pyqtgraphWidget.removeItem(self.allPlotsDict['{}'.format(indicator)]['plotItem'])
            self.allPlotsDict[indicator]['displayed'] = 0
            self.update_plots_position()

        else:
            pass

    def update_plots_position(self):
        self.pyqtgraphWidget.clear()
        sideLength = math.ceil(
            math.sqrt(sum(self.allPlotsDict[ind]['displayed'] == 1 for ind in self.allPlotsDict.keys())))
        tempPlotDict = {key : value for (key, value) in self.allPlotsDict.items() if value['displayed'] == 1}
        indicatorList = list(tempPlotDict.keys())
        listIndex = 0
        for i in range(sideLength):
            for j in range(sideLength):
                try:
                    self.pyqtgraphWidget.addItem(tempPlotDict[indicatorList[listIndex]]['plotItem'], i, j)
                    listIndex += 1
                except:
                    pass

    @pyqtSlot(dict)
    def update_graph(self, simPlotData):
        # all plot are updated, but could verify which one is active and only update those
        #print(simPlotData)
        for indicator in Person().indicators:
            for ageGroup in Person().ageGroupsList:
                try:
                    kwargs = simPlotData[indicator][ageGroup]
                    self.allPlotsDict[indicator]['plotDataItem'].setData(**kwargs)
                except:
                    log.info('null')

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
        self.pb_simulate.setEnabled(False)
        self.pb_simulate.clicked.disconnect()
        self.pb_simulate.clicked.connect(self.stop_simulation)
        self.pb_simulate.setText("Stop")
        self.pb_simulate.setEnabled(True)
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

    def stop_simulation(self):
        self.pb_simulate.setEnabled(False)
        self.pb_simulate.setText("Resume")
        self.simulationThread.setTerminationEnabled(True)
        self.simulationThread.terminate()
        self.pb_simulate.clicked.disconnect()
        self.pb_simulate.clicked.connect(self.resume_simulation)
        self.pb_simulate.setEnabled(True)

    def resume_simulation(self):
        pass
