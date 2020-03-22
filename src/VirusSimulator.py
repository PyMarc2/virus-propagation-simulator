import random
import numpy as np
import matplotlib.pyplot as plt
import json
from PyQt5.QtCore import pyqtSignal, QObject
import datetime
import logging

log = logging.getLogger(__name__)


class VirusSimulator(QObject):
    s_data_changed = pyqtSignal(list)
    
    def __init__(self):
        super(VirusSimulator, self).__init__()
        self.timeNow = 0
        self.timePast = 0
        self.day = 0
        self.selectedIndicators = []
        self.population = []
        self.parameters = {}
        self.statusByAgeGroup = {}
        self.healthcareSystemLimit = 50000

    def simulate_from_gui(self, *args, **kwargs):
        self.create_population(args[0])
        self.initialize_infection(nbOfInfected=args[1])
        self.launch_propagation(args[2])

    def simulate(self, amount, time, parameters):
        self.create_population(amount, parameters)
        self.initialize_infection(nbOfInfected=1)
        self.launch_propagation(time)

    def plot_results(self, indicator):
        fig, ax1 = plt.subplots(figsize=(4, 4))
        xdata = range(len(self.statusByAgeGroup))

        for ageKey in self.statusByAgeGroup[0].keys():
            data2plot = []
            for dayKey in self.statusByAgeGroup.keys():
                data2plot.append(self.statusByAgeGroup[int(dayKey)][ageKey][indicator])
            ax1.plot(xdata, data2plot, label=ageKey)

        ax1.legend()
        plt.show()

    def send_data_to_plot(self, indicators=None):
        if indicators is not None:
            self.selectedIndicators = indicators

        xdata = list(range(len(self.statusByAgeGroup)))

        for ageKey in self.statusByAgeGroup[0].keys():
            data2plot = []
            for j, indicator in enumerate(self.selectedIndicators):
                data2plot.append([])
                for dayKey in self.statusByAgeGroup.keys():
                    data2plot[j].append(self.statusByAgeGroup[int(dayKey)][ageKey][indicator])
                self.s_data_changed.emit([xdata, data2plot])

    def send_results(self, indicator):
        xdata = range(len(self.statusByAgeGroup))

        for ageKey in self.statusByAgeGroup[0].keys():
            data2plot = []
            for dayKey in self.statusByAgeGroup.keys():
                data2plot.append(self.statusByAgeGroup[int(dayKey)][ageKey][indicator])
            self.s_data_changed.emit(data2plot)

    def launch_propagation(self, nbOfDays):

        for d in range(nbOfDays):
            self.day = d
            log.info('Simulation Day: {} on {} ({}%)'.format(d, nbOfDays-1, d * 100 / nbOfDays-1))
            self.statusByAgeGroup[d] = {}
            for group in self.parameters.keys():
                self.statusByAgeGroup[d][group] = {}

            self.meet_people()
            log.info('DAY {} :: BEGIN SAVE STATUS'.format(d))
            self.save_status(d)
            log.info('DAY {} :: END SAVE STATUS'.format(d))

            #print(self.statusByAgeGroup)
            self.send_data_to_plot()


        log.info('=== === === SIMULATION COMPLETE === === ===')

    def meet_people(self):
        log.info('DAY {} :: BEGIN INDEXING'.format(self.day))
        personListIndex = [i if x.isInfected == 1 else -1 for i, x in enumerate(self.population)]
        personListIndex = list(filter((-1).__ne__, personListIndex))
        log.info('DAY {} :: END INDEXING'.format(self.day))

        log.info('DAY {} :: BEGIN MEETING PERSONS'.format(self.day))
        liste = [self.population[i] for i in personListIndex]
        for person in liste:
            person.update_own_status()
            if person.isInfectious:
                for metPerson in range(int(person.parameters['knownEncounteredPerDay'])):
                    person.interact(random.choice(person.listOfRelatives))
        log.info('DAY {} :: END MEETING PERSONS'.format(self.day))

    def save_status(self, d):
        for key in self.statusByAgeGroup[d].keys():
            self.statusByAgeGroup[d][key]['isInfected'] = (
                sum(p.isInfected == 1 and p.tag == key for p in self.population))
            # self.statusByAgeGroup[d][key]['isInfectious'] = (
            #     sum(p.isInfectious == 1 and p.tag == key for p in self.population))
            self.statusByAgeGroup[d][key]['isAlive'] = (
                sum(p.isAlive == 1 and p.tag == key for p in self.population))
            # self.statusByAgeGroup[d][key]['isReachable'] = (
            #     sum(p.isReachable == 1 and p.tag == key for p in self.population))
            self.statusByAgeGroup[d][key]['hasSymptoms'] = (
                sum(p.hasSymptoms == 1 and p.tag == key for p in self.population))
            self.statusByAgeGroup[d][key]['isRecovered'] = (
                sum(p.isRecovered == 1 and p.tag == key for p in self.population))

    def initialize_infection(self, nbOfInfected=1):
        try:
            indexes = random.choices(range(len(self.population)), k=nbOfInfected)
            for index in indexes:
                self.population[index].isInfected = 1
        except Exception as e:
            log.error(e)

    def create_population(self, amountOfPeople, parameters=None):
        if parameters is not None:
            self.parameters = parameters

        id = 0
        for i, key in enumerate(self.parameters.keys()):
            for j in range(int(amountOfPeople * self.parameters[key]['percentageOfPopulation'])):
                randomizedParameters = self.give_gaussian_parameters(self.parameters[key])
                self.population.append(Person(randomizedParameters, tag=key, id=id))
                id += 1
            print('creating population...{}/{}'.format(i, len(self.parameters.keys())))
        random.shuffle(self.population)
        print('population Created')
        print('selecting mates...')
        for person in self.population:
            person.select_relatives(self.population)
        print('mates selected')
        return self.population

    def load_json_parameters(self, jsonFilePath):
        with open(jsonFilePath) as f:
            parametersFile = json.load(f)
        self.parameters = parametersFile[0]
        return self.parameters

    @staticmethod
    def give_gaussian_parameters(parameters):
        randomizedParameters = {'knownEncounteredPerDay': None,
                                'probabilityOfInfection': None,
                                'timeOfIncubation': None,
                                'timeBeforeNonInfectious': None,
                                'timeBeforeInfectious': None,
                                'timeOfPeakSymptoms': None,
                                'timeOfRecuperation': None,
                                'probabilityOfDying': None}
        # print(parameters)
        parameters.pop('percentageOfPopulation', None)

        for parameter in parameters:
            randomizedParameters[parameter] = np.random.normal(loc=parameters[parameter]['mean'],
                                                               scale=parameters[parameter]['sd'])

        return randomizedParameters


class Person:
    def __init__(self, parameters, tag=None, id=None):
        self.id = id
        self.tag = tag
        self.parameters = {'knownEncounteredPerDay': parameters['knownEncounteredPerDay'],
                           'unwantedEncounteredPerDay': parameters['unwantedEncounteredPerDay'],
                           'probabilityOfInfection': parameters['probabilityOfInfection'],
                           'timeBeforeInfectious': parameters['timeBeforeInfectious'],
                           'timeOfIncubation': parameters['timeOfIncubation'],
                           'timeOfPeakSymptoms': parameters['timeOfPeakSymptoms'],
                           'probabilityOfDying': parameters['probabilityOfDying'],
                           'timeOfRecuperation': parameters['timeOfRecuperation'],
                           'timeBeforeNonInfectious': parameters['timeBeforeNonInfectious']}

        self.listOfRelatives = []
        self.timeSinceInfection = 0
        self.isReachable = 1
        self.needsMedicalAttention = 0
        self.isHospitalised = 0
        self.isAlive = 1
        self.isInfected = 0
        self.isInfectious = 0
        self.hasSymptoms = 0
        self.isRecovered = 0

    def select_relatives(self, listOfPeople):
        self.listOfRelatives = random.choices(listOfPeople, k=100)

    def update_own_status(self):
        if self.isAlive:
            if self.isInfected:
                self.timeSinceInfection += 1

                if self.timeSinceInfection >= self.parameters['timeBeforeInfectious']:
                    self.isInfectious = 1

                if self.timeSinceInfection >= self.parameters['timeOfIncubation']:
                    self.hasSymptoms = 1

                if self.timeSinceInfection >= self.parameters['timeOfPeakSymptoms']:
                    self.needsMedicalAttention = 1
                    # needs to test if hospitals are full, if they are launch tryDie() function.

                if self.timeSinceInfection >= self.parameters['timeOfRecuperation']:
                    self.hasSymptoms = 0
                    self.isInfected = 0
                    self.isRecovered = 0

                if self.timeSinceInfection >= self.parameters['timeBeforeNonInfectious']:
                    self.isInfectious = 0

    def interact(self, person):
        if person.isInfectious:
            if not self.isRecovered:
                if random.choices([0, 1], weights=[1 - self.parameters['probabilityOfInfection'],
                                                   self.parameters['probabilityOfInfection']]):
                    self.isInfected = 1

        elif self.isInfectious:
            if not person.isInfectious and not person.isRecovered:
                if random.choices([0, 1], weights=[1 - person.parameters['probabilityOfInfection'],
                                                   person.parameters['probabilityOfInfection']]):
                    person.isInfected = 1

    def goto_hospital(self):
        pass
