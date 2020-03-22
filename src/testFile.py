import logging
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QSettings
from VirusSimulator import VirusSimulator
import os

sim = VirusSimulator()
defaultFilePath = os.path.dirname(os.path.realpath(__file__)) + r'\parameters_preset\default_parameters.json'
sim.load_json_parameters(defaultFilePath)