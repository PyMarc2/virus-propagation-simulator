
import json
from VirusSimulator import VirusSimulator

with open("quebec_params.json") as f:
  parameters_quebec = json.load(f)

COVID19 = VirusSimulator()
COVID19.simulate(80000, 40, parameters_quebec[0])
