import logging
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QSettings
from VirusSimulator import VirusSimulator


log = logging.getLogger(__name__)


class MainModel(QObject):
    s_simulatorObject_changed = pyqtSignal(VirusSimulator)

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
