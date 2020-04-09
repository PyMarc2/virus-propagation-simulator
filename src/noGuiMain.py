from VirusSimulator import VirusSimulator
from Person import Person
import os

COVID19 = VirusSimulator()
defaultFilePath = os.path.dirname(os.path.realpath(__file__)) + r"\parameters_preset\default_parameters.json"
COVID19.load_json_parameters(defaultFilePath)

COVID19.simulate(10000, 50)