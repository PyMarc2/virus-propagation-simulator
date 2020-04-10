from PyQt5.QtWidgets import QWidget, QLineEdit, QSlider
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QMutex
from PyQt5.Qt import QIntValidator
from pyqtgraph import PlotItem
from tools.threadWorker import Worker
from pydispatch import dispatcher
from tools.stoppableThread import QStoppableThread
from tools.prettyPrint import pretty
from Person import Person
import os
import json
from PyQt5 import uic
import logging
import math
import threading

log = logging.getLogger(__name__)

simulationViewUiPath = os.path.dirname(os.path.realpath(__file__)) + "\\simulationViewUi.ui"
Ui_simulationView, QtBaseClass = uic.loadUiType(simulationViewUiPath)

SIGNAL_PLOT_TOGGLED = "plot.toggled.indicator"


class SimulationView(QWidget, Ui_simulationView):
    SIGNAL_toggled_plot_indicator = "indicator"

    # TODO: Connect slidders to editTextBox to variable population/time/etc...
    # TODO: By default set to ['ALL'] age group
    # TODO: Possibility to BAR GRAPH PLOT
    # TODO: Customizable graph parameters
    # TODO: Toggle betwwen fitting mode and free simulation mode
    # TODO: Code the Fitting Mode Backend ( REALLY HARD new branch for this)
    # TODO: Button STOP and RESET working
    # TODO: separation button
    # TODO: find a way ofr more efficient computing

    def __init__(self, model=None, controller=None):
        super(SimulationView, self).__init__()
        self.model = model
        self.allPlotsDict = {}
        self.setupUi(self)
        self.setup_buttons()
        self.connect_buttons()
        self.connect_signals()
        self.create_plots()
        self.initialize_view()

    def initialize_view(self):
        self.cb_isInfected.setChecked(True)
        self.rb_freeSimulation.setChecked(True)
        self.le_population.setText("10000")
        self.le_simulationTime.setText("100")
        self.le_nbOfInfected.setText("1")

    def setup_buttons(self):
        self.le_population.setValidator(QIntValidator())
        self.le_simulationTime.setValidator(QIntValidator())
        self.le_nbOfInfected.setValidator(QIntValidator())
        self.onHsPress = 0
        self.hs_population.setMaximum(100000)
        self.hs_population.setMinimum(1000)
        self.hs_population.setSingleStep(1000)
        self.hs_simulationTime.setMaximum(365)
        self.hs_simulationTime.setMinimum(10)
        self.hs_nbOfInfected.setMaximum(1000)
        self.hs_nbOfInfected.setMinimum(1)
        self.populationBtnGroup = {"la":self.la_population, "le":self.le_population, "hs":self.hs_population}
        self.simulationTimeBtnGroup = {"la": self.la_simulationTime, "le": self.le_simulationTime, "hs": self.hs_simulationTime}
        self.nbOfInfectedBtnGroup = {"la": self.la_nbOfInfected, "le": self.le_nbOfInfected, "hs": self.hs_nbOfInfected}

    def setOnHsPress(self, value):
        self.onHsPress = value  # type: bool

    def connect_buttons(self):
        log.debug("Connecting simulationView GUI...")
        # MAIN BUTTONS
        self.pb_simulate.clicked.connect(self.launch_simulation)

        # RADIO BOXES
        self.rb_freeSimulation.toggled.connect(self.toggle_free_simulation)
        self.rb_fittingSimulation.toggled.connect(self.toggle_fitting_simulation)

        # BASIC PARAMETERS
        self.hs_population.sliderMoved.connect(lambda: self.setOnHsPress(True))
        self.hs_simulationTime.sliderMoved.connect(lambda: self.setOnHsPress(True))
        self.hs_nbOfInfected.sliderMoved.connect(lambda: self.setOnHsPress(True))

        self.hs_population.valueChanged.connect(
            lambda: self.update_free_simulation_parameters(group=self.populationBtnGroup, caller="hs"))
        self.hs_simulationTime.valueChanged.connect(
            lambda: self.update_free_simulation_parameters(group=self.simulationTimeBtnGroup, caller="hs"))
        self.hs_nbOfInfected.valueChanged.connect(
            lambda: self.update_free_simulation_parameters(group=self.nbOfInfectedBtnGroup, caller="hs"))
        self.le_population.textChanged.connect(
            lambda: self.update_free_simulation_parameters(group=self.populationBtnGroup, caller="le"))
        self.le_simulationTime.textChanged.connect(
            lambda: self.update_free_simulation_parameters(group=self.simulationTimeBtnGroup, caller="le"))
        self.le_nbOfInfected.textChanged.connect(
            lambda: self.update_free_simulation_parameters(group=self.nbOfInfectedBtnGroup, caller="le"))
        log.debug("Connections Established")

        # CHECKBOXES
        self.cb_isInfected.stateChanged.connect(lambda: self.toggle_plot("isInfected", caller=self.cb_isInfected))
        self.cb_isInfectious.stateChanged.connect(lambda: self.toggle_plot("isInfectious", caller=self.cb_isInfectious))
        self.cb_isAlive.stateChanged.connect(lambda: self.toggle_plot("isAlive", caller=self.cb_isAlive))
        self.cb_isRecovered.stateChanged.connect(lambda: self.toggle_plot("isRecovered", caller=self.cb_isRecovered))
        self.cb_isHospitalized.stateChanged.connect(
            lambda: self.toggle_plot("isHospitalized", caller=self.cb_isHospitalized))
        self.cb_hasSymptoms.stateChanged.connect(lambda: self.toggle_plot("hasSymptoms", caller=self.cb_hasSymptoms))

    def connect_signals(self):
        log.debug("Connecting simulationView Signals...")
        self.model.simulatorObject.s_data_changed.connect(self.update_graph)

    def update_free_simulation_parameters(self, group, caller):
        if caller == "hs":
            if self.onHsPress:
                group["le"].setText(str(group[caller].value()))
                self.setOnHsPress(False)
        elif caller == "le":
            if group[caller].text() == '':
                group["hs"].setValue(0)
            else:
                group["hs"].setValue(int(group[caller].text()))
        self.model.populationSize = int(self.le_population.text())
        self.model.simulationTime = int(self.le_simulationTime.text())
        self.model.initialInfected = int(self.le_nbOfInfected.text())

    def toggle_free_simulation(self):
        if self.rb_freeSimulation.isChecked:
            self.freeSimulationWidget.setEnabled(True)
            self.fittingSimulationWidget.setEnabled(False)

    def toggle_fitting_simulation(self):
        if self.rb_fittingSimulation.isChecked:
            self.freeSimulationWidget.setEnabled(False)
            self.fittingSimulationWidget.setEnabled(True)

    def create_plots(self):
        for indicator in Person().indicators:
            self.allPlotsDict[indicator] = {"plotItem": PlotItem(), "displayed": 0}
        for indicator in Person().indicators:
            self.allPlotsDict[indicator]["plotDataItem"] = {}
            for ageGroup in Person().ageGroupsList:
                dataPlotItem = self.allPlotsDict[indicator]["plotItem"].plot()
                self.allPlotsDict[indicator]["plotDataItem"][ageGroup] = dataPlotItem
                # self.allPlotsDict[indicator]["plotDataItem"][ageGroup].setDownsampling()
            self.allPlotsDict[indicator]["plotItem"].setTitle(indicator)
        print(self.allPlotsDict)

    def toggle_plot(self, indicator, caller=None):
        if caller.checkState() == 2:
            self.allPlotsDict[indicator]["displayed"] = 1
            self.update_plots_position()
            dispatcher.send(signal=SIGNAL_PLOT_TOGGLED, sender=self, **{"indicator":indicator})

        elif caller.checkState() == 0:
            self.pyqtgraphWidget.removeItem(self.allPlotsDict["{}".format(indicator)]["plotItem"])
            self.allPlotsDict[indicator]["displayed"] = 0
            self.update_plots_position()

        else:
            pass

    def update_plots_position(self):
        self.pyqtgraphWidget.clear()
        sideLength = math.ceil(
            math.sqrt(sum(self.allPlotsDict[ind]["displayed"] == 1 for ind in self.allPlotsDict.keys())))
        tempPlotDict = {key : value for (key, value) in self.allPlotsDict.items() if value["displayed"] == 1}
        indicatorList = list(tempPlotDict.keys())
        listIndex = 0
        for i in range(sideLength):
            for j in range(sideLength):
                try:
                    self.pyqtgraphWidget.addItem(tempPlotDict[indicatorList[listIndex]]["plotItem"], i, j)
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
                    #print(ageGroup)
                    self.allPlotsDict[indicator]["plotDataItem"][ageGroup].setData(**kwargs)
                except:
                    log.debug("null")

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

    def launch_simulation(self):
        if self.rb_freeSimulation.isChecked:
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
        elif self.rb_fittingSimulation.isChecked:
            pass

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
