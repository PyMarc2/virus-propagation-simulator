import matplotlib.pyplot as plt
import json
from VirusSimulator import VirusSimulator

with open("quebec_params.json") as f:
  parameters_quebec = json.load(f)


COVID19 = VirusSimulator()
COVID19.simulate(8000000, 90, parameters_quebec[0])
print(COVID19.statusByAgeGroup)

fig, ax1 = plt.subplots(figsize=(4, 4))

wantedStatus = 'isInfected'
xdata = range(len(COVID19.statusByAgeGroup))

for ageKey in COVID19.statusByAgeGroup[0].keys():
    data2plot = []
    for dayKey in COVID19.statusByAgeGroup.keys():
        data2plot.append(COVID19.statusByAgeGroup[int(dayKey)][ageKey][wantedStatus])
    ax1.plot(xdata, data2plot, label=ageKey)

ax1.legend()
plt.show()
