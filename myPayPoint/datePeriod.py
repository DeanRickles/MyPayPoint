import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td

def compare_datetime_list(reference, difference):
    # reference:  Specifies an array of objects used as a reference for comparison.
    # difference: Specifies the objects that are compared to the reference objects.
    return list( set(reference).difference(set(difference)) )

def datespan(datetime, enddatetime):
    # Requirements: pip install pandas
    # startDate example: datetime(2021,7,14,0,0,0)
    # endDate example:   datetime.today()
    return pd.date_range( end   = enddatetime.replace(microsecond=0, second=0, minute=0), 
                          start = datetime.replace(microsecond=0, second=0, minute=0),
                         freq   = 'H').strftime("%d/%m/%Y %H:%M:%S").tolist()


def filter_workday(datetime):
    # Setup to my own hours wanted. Need to review a better solution.
    lst = []
    for x in datetime:
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



def hour_end(datetime):
    lst = []
    for x in datetime:
        if isinstance(x, str):
            lst.append(x.replace(':00:00',':59:59'))
        else:
            print(f"hour_end() error: {x} is not a str date.")
            break
    return lst



def hour_rounder(datetime):
    lst = []
    for t in datetime:
        if isinstance(t, str):
            lst.append(t[:14] + '00:00')
        else:
            lst.append(t.replace(second=0, microsecond=0, minute=0, hour=t.hour) +timedelta(hours=t.minute//30))
    return lst



def distinct_datetime(datetime):
    return list(set(datetime))