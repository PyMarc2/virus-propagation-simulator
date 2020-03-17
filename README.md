# Virus Propagation Simulator

This simulator was built during the COVID-19 erruption. The world is in chaos ahah.
Instead of looking at the brownian simulation that everyone is so optimistic about, I wanted to be sure that the curves they were showing matched the profile of a real simulation with lots of parameters. It took me a day to think about it and code it, so don't expect too much. _We are more interested in the curves it produces than in the actual numbers, since there are many parameters that aren't really precise._


## - JSON population's parameters file
A JSON file contains all the population information on every possible parameter. View the .json in the project to understand. Each parameter has a _mean_ and a _standard deviation_ from which we will later distribute randomly those parameters according to a gaussian curve with the same _mean_ and _sd_.

## - Person class

encapsulate all the following parameters:
    
    'knownEncounteredPerDay': 
    'unwantedEncounteredPerDay':
    'probabilityOfInfection'
    'timeBeforeInfectious'
    'timeOfIncubation'
    'timeOfPeakSymptoms'
    'probabilityOfDying'
    'timeOfRecuperation'
    'timeBeforeNonInfectious'
    'willQuarantine'

All those parameters are decided in the `VirusSimulator` class. They are distributed according to the gaussian curve generated with the _mean_ and _sd_ in the .json.

and a `Person` encapsulates all the following states:
        
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
 
