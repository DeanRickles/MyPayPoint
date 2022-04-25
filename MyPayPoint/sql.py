import psycopg
from datetime import datetime

def SQLGetSalesDates():
    '''
        Requirement:
            pip install psycopg-binary psycopg
            
        possibly add how may days back to query?
    '''

    ''' SQL Variables
    '''
    vServerIP   = ''
    vServerPort = ''
    vServerDB   = ''
    vServerUser = ''
    vServerPass = ''
    
    ''' Connect to Databasse
    '''
    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB, 
                            user=vServerUser, 
                            password=vServerPass, 
                            host=vServerIP, 
                            port=vServerPort)
     
    vConn.autocommit = True
    
    # Open a cursor to proform database operations.
    vCurr = vConn.cursor()
    
    ''' SQL execute
    '''
    
    # execute command
    vCurr.execute('''SELECT DISTINCT startdate
                  from public.reportdata;''')
    
    # fetch mutli line
    reportdataStartDate = vCurr.fetchall()
    
    lst = []
    for x in sorted(reportdataStartDate, reverse=True):
        lst.append(datetime.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))
    
    vCurr.close()
    
    return lst


def SQLGetTenderDates():
    '''
        Requirement:
            pip install psycopg-binary psycopg
            
        possibly add how may days back to query?
    '''
    
    ''' SQL Variables
    '''
    vServerIP   = ''
    vServerPort = ''
    vServerDB   = ''
    vServerUser = ''
    vServerPass = ''
    
    ''' Connect to Databasse
    '''
    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB, 
                            user=vServerUser, 
                            password=vServerPass, 
                            host=vServerIP, 
                            port=vServerPort)
     
    vConn.autocommit = True
    
    # Open a cursor to proform database operations.
    vCurr = vConn.cursor()
    
    ''' SQL execute
    '''
    
    # execute command
    vCurr.execute('''SELECT DISTINCT cast(CONCAT(LEFT(cast(datetime as text), 14),'00:00') as timestamp) as datetime
                  from public.tenderdata;''')
    
    # fetch mutli line
    reportdataStartDate = vCurr.fetchall()
    
    lst = []
    for x in sorted(reportdataStartDate, reverse=True):
        lst.append(datetime.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))
    
    vCurr.close()
    
    return lst



def SQLGetPPIDDates():
    '''
        Requirement:
            pip install psycopg-binary psycopg
            
        possibly add how may days back to query?
    '''
    
    ''' SQL Variables
    '''
    vServerIP   = ''
    vServerPort = ''
    vServerDB   = ''
    vServerUser = ''
    vServerPass = ''
    
    ''' Connect to Databasse
    '''
    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB, 
                            user=vServerUser, 
                            password=vServerPass, 
                            host=vServerIP, 
                            port=vServerPort)
     
    vConn.autocommit = True
    
    # Open a cursor to proform database operations.
    vCurr = vConn.cursor()
    
    ''' SQL execute
    '''
    
    # execute command
    vCurr.execute('''SELECT DISTINCT cast(CONCAT(LEFT(cast(date_time as text), 14),'00:00') as timestamp) as date_time
                  from public.ppiddata;''')
    
    # fetch mutli line
    reportdataStartDate = vCurr.fetchall()
    
    lst = []
    for x in sorted(reportdataStartDate, reverse=True):
        lst.append(datetime.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))
    
    vCurr.close()
    
    return lst
