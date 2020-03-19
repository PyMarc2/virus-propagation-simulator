
import json
from src.VirusSimulator import VirusSimulator

with open("parameters_preset/quebec_params.json") as f:
  parameters_quebec = json.load(f)

COVID19 = VirusSimulator()
COVID19.simulate(80000, 40, parameters_quebec[0])
