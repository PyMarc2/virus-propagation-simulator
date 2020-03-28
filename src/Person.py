import random


class Person:
    def __init__(self, globalParameters=None, tag=None, id=None):
        self.id = id
        self.tag = tag
        if globalParameters is not None:
            self.parameters = {'knownEncounteredPerDay': globalParameters['knownEncounteredPerDay'],
                           'unwantedEncounteredPerDay': globalParameters['unwantedEncounteredPerDay'],
                           'probabilityOfInfection': globalParameters['probabilityOfInfection'],
                           'timeBeforeInfectious': globalParameters['timeBeforeInfectious'],
                           'timeOfIncubation': globalParameters['timeOfIncubation'],
                           'timeOfPeakSymptoms': globalParameters['timeOfPeakSymptoms'],
                           'probabilityOfDying': globalParameters['probabilityOfDying'],
                           'timeOfRecuperation': globalParameters['timeOfRecuperation'],
                           'timeBeforeNonInfectious': globalParameters['timeBeforeNonInfectious']}

        self.listOfRelatives = []
        self.ageGroupsList = ['[0-9]', '[10-19]','[20-29]','[30-39]','[40-49]','[50-59]','[60-69]','[70-79]','[80-89]', '[90-99]']
        self.indicators = {'timeSinceInfection': 0,
                           'isQuarantined': 1,
                           'needsMedicalAttention': 0,
                           'isHospitalized': 0,
                           'isAlive': 1,
                           'isInfected': 0,
                           'isInfectious': 0,
                           'hasSymptoms': 0,
                           'isRecovered': 0}

    def select_relatives(self, listOfPeople):
        self.listOfRelatives = random.choices(listOfPeople, k=100)

    def update_own_status(self):
        if self.indicators['isAlive']:
            if self.indicators['isInfected']:
                self.indicators['timeSinceInfection'] += 1

                if self.indicators['timeSinceInfection'] >= self.parameters['timeBeforeInfectious']:
                    self.indicators['isInfectious'] = 1

                if self.indicators['timeSinceInfection'] >= self.parameters['timeOfIncubation']:
                    self.indicators['hasSymptoms'] = 1

                if self.indicators['timeSinceInfection'] >= self.parameters['timeOfPeakSymptoms']:
                    self.indicators['needsMedicalAttention'] = 1
                    # needs to test if hospitals are full, if they are launch tryDie() function.

                if self.indicators['timeSinceInfection'] >= self.parameters['timeOfRecuperation']:
                    self.indicators['hasSymptoms'] = 0
                    self.indicators['isInfected'] = 0
                    self.indicators['isRecovered'] = 0

                if self.indicators['timeSinceInfection'] >= self.parameters['timeBeforeNonInfectious']:
                    self.indicators['isInfectious'] = 0

    def interact(self, person):
        if person.indicators['isInfectious']:
            if not self.indicators['isRecovered']:
                if random.choices([0, 1], weights=[1 - self.parameters['probabilityOfInfection'],
                                                   self.parameters['probabilityOfInfection']]):
                    self.indicators['isInfected'] = 1

        elif self.indicators['isInfectious']:
            if not person.indicators['isInfectious'] and not person.indicators['isRecovered']:
                if random.choices([0, 1], weights=[1 - person.parameters['probabilityOfInfection'],
                                                   person.parameters['probabilityOfInfection']]):
                    person.indicators['isInfected'] = 1

    def goto_hospital(self):
        pass

