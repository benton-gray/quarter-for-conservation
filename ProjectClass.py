#definition of Project Class
#from array import array
class Project:
    segmentData = 0
    segmentClock = 0
    segmentLatch = 0
    firstInterrupt = 0
    secondInterrupt = 0
    storedNumberFileName = ""
    currentNumber = 0
    
    def init(self,segmentLatch,segmentClock,segmentData,storedNumberFileName,firstInterrupt,secondInterrupt,currentNumber):
        self.segmentData = segmentData
        self.segmentClock = segmentClock
        self.segmentLatch = segmentLatch
        self.storedNumberFileName = storedNumberFileName
        self.firstInterrupt = firstInterrupt
        self.secondInterrupt = secondInterrupt
        self.currentNumber = currentNumber