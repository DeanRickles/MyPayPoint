import pandas as pd
from datetime import datetime

def compareDateList(vReference, vDifference):
    '''
        Variables:
            vReference
                Specifies an array of objects used as a reference for comparison.
            vDifference
                Specifies the objects that are compared to the reference objects.
    '''
    lst = list( set(vReference).difference(set(vDifference)))
    return lst


def dateSpan(vStartDate, vEndDate):
    '''
        Requirements:
            pip install pandas

        Variables:
            startDate example:
                datetime(2021,7,14,0,0,0)

            endDate example:
                datetime.today()
    '''
    return pd.date_range( end   = vEndDate.replace(microsecond=0, second=0, minute=0), 
                          start = vStartDate.replace(microsecond=0, second=0, minute=0),
                         freq   = 'H').strftime("%d/%m/%Y %H:%M:%S").tolist()



def filterWorkDay(vTimestamp):
    '''
        Setup to my own hours wanted.
        Need to review a better solution.
    '''
    lst = []
    for x in vTimestamp:
        if ' 00' in x:
            pass
        elif ' 01' in x:
            pass
        elif ' 02' in x:
            pass
        elif ' 03' in x:
            pass
        elif ' 04' in x:
            pass
        elif ' 05' in x:
            pass
        elif ' 06' in x:
            lst.append(x)
        elif ' 07' in x:
            lst.append(x)
        elif ' 08' in x:
            lst.append(x)
        elif ' 09' in x:
            lst.append(x)
        elif ' 10' in x:
            lst.append(x)
        elif ' 11' in x:
            lst.append(x)
        elif ' 12' in x:
            lst.append(x)
        elif ' 13' in x:
            lst.append(x)
        elif ' 14' in x:
            lst.append(x)
        elif ' 15' in x:
            lst.append(x)
        elif ' 16' in x:
            lst.append(x)
        elif ' 17' in x:
            lst.append(x)
        elif ' 18' in x:
            lst.append(x)
        elif ' 19' in x:
            lst.append(x)
        elif ' 20' in x:
            lst.append(x)
        elif ' 21' in x:
            lst.append(x)
        elif ' 22' in x:
            lst.append(x)
        elif ' 23' in x:
            pass
        elif ' 24' in x:
            pass   
    return lst



def reportHoulyEnd(vTimestamp):
    '''
        Doesn't work save for later.
    '''
    
    lst = []
    for x in vTimestamp:
        start = x
        end = x.replace(':00:00',':59:59')
        y = (end)
        lst.append(y)
        
    return lst