**Virus Propagation Simulator**

This simulator was built during the COVID-19 erruption. The world is in chaos ahah.
Instead of looking at the brownian simulation that everyone is so optimistic about, I wanted to be sure that the curves they were showing matched the profile of a real simulation with lots of parameters. It took me a day to think about it and code it, so don't expect too much._We are more interested in the curves it produces than in the actual numbers, since there are many parameters that aren't really precise._

**Person class**

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

and all the following states:
        
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
