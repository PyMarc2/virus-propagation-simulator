import logging
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QSettings
from VirusSimulator import VirusSimulator
import os


log = logging.getLogger(__name__)


class MainModel(QObject):
    s_simulatorObject_changed = pyqtSignal(VirusSimulator)
    defaultFilePath = os.path.dirname(os.path.realpath(__file__)) + r"\parameters_preset\default_parameters.json"
    alternativePath = "default_parameters.json"
    print(defaultFilePath)

    def __init__(self):
        super(MainModel, self).__init__()
        self._simulatorObject = VirusSimulator()
        self._initialInfected = 1
        self._populationSize = 10000
        self._simulationTime = 60
        self._simulatorObject.load_json_parameters(self.defaultFilePath)
        self._loadedPopulationParameters = self._simulatorObject.parameters
        self.selectedIndicators = []


    @property
    def simulatorObject(self):
        return self._simulatorObject

    @simulatorObject.setter
    def simulatorObject(self, value):
        self._simulatorObject = value
        log.warning("simulatorObject has been CHANGED")

    @simulatorObject.deleter
    def simulatorObject(self):
        del self._simulatorObject
        log.warning("simulatorObject has been DELETED")

    @property
    def populationSize(self):
        return self._populationSize

    @populationSize.setter
    def populationSize(self, value):
        self._populationSize = value
        log.debug("populationSize has been CHANGED")

    @property
    def simulationTime(self):
        return self._simulationTime

    @simulationTime.setter
    def simulationTime(self, value):
        self._simulationTime = value
        log.debug("simulationTime has been CHANGED")

    @property
    def initialInfected(self):
        return self._initialInfected

    @initialInfected.setter
    def initialInfected(self, value):
        self._initialInfected = value
        log.debug("initialInfected has been CHANGED")

    @property
    def loadedPopulationParameters(self):
        return self._loadedPopulationParameters

    @loadedPopulationParameters.setter
    def loadedPopulationParameters(self, value):
        self._loadedPopulationParameters = self._simulatorObject.load_json_parameters(value)
        log.debug("LoadedPopulationParameters has been CHANGED. Location is: {}".format(value))

    @property
    def selectedIndicators(self):
        return self._selectedIndicators

    @selectedIndicators.setter
    def selectedIndicators(self, value):
        self._selectedIndicators = value
        self._simulatorObject.selectedIndicators = value
        log.debug("selectedIndicators has been CHANGED")
