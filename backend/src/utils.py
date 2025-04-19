from datetime import datetime, timedelta

def checkIfExpired( startDate : datetime, duration : int, currentDate : datetime ) -> bool:
    endDate = startDate + timedelta(days=duration)
    return endDate < currentDate

def getStartDateOfCurrentCycle(startOfLastCycle : datetime, 
                               duration : int, 
                               currentDate : datetime ) -> datetime:
    startDateOfCurrentCycle = startOfLastCycle + timedelta(days = duration + 1)
    
    while checkIfExpired(startDateOfCurrentCycle + timedelta(days=duration), duration, currentDate):
        startDateOfCurrentCycle = startDateOfCurrentCycle + timedelta(days=duration)
    
    return startDateOfCurrentCycle
