from datetime import datetime, timedelta

def checkIfExpired( startDate : datetime, duration : int, currentDate : datetime ) -> bool:
    endDate = startDate + timedelta(days=duration-1)
    return endDate < currentDate

def getStartDateOfCurrentCycle(startOfLastCycle : datetime, 
                               duration : int, 
                               currentDate : datetime ) -> datetime:
    difference = (currentDate - startOfLastCycle).days
    cyclesSkipped = difference // duration

    startDateOfCurrentCycle = startOfLastCycle + timedelta(days = duration * cyclesSkipped)
    
    return startDateOfCurrentCycle
