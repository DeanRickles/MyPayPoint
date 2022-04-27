import psycopg
from datetime import datetime

def GetSalesDates(vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Requirement:
            pip install psycopg-binary psycopg
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
    
    # execute command
    vCurr.execute(f'''SELECT DISTINCT startdate
                  from public.{vServerTbl};''')
    
    # fetch mutli line
    reportdataStartDate = vCurr.fetchall()
    
    lst = []
    for x in sorted(reportdataStartDate, reverse=True):
        lst.append(datetime.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))
    
    # close connection.
    vCurr.close()
    
    # cleanup variables.
    del vCurr, vConn, reportdataStartDate
    
    return lst


def GetTenderDates(vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Requirement:
            pip install psycopg-binary psycopg
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
    
    # execute command
    vCurr.execute(f'''SELECT DISTINCT cast(CONCAT(LEFT(cast(datetime as text), 14),'00:00') as timestamp) as datetime
                  from public.{vServerTbl};''')
    
    # fetch mutli line
    reportdataStartDate = vCurr.fetchall()
    
    lst = []
    for x in sorted(reportdataStartDate, reverse=True):
        lst.append(datetime.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))

    # close connection.
    vCurr.close()
    
    # cleanup variables.
    del vCurr, vConn, reportdataStartDate
    
    return lst


def GetPPIDDates(vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Requirement:
            pip install psycopg-binary psycopg
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
    
    # execute command
    vCurr.execute(f'''SELECT DISTINCT cast(CONCAT(LEFT(cast(date_time as text), 14),'00:00') as timestamp) as date_time
                  from public.{vServerTbl};''')
    
    # fetch mutli line
    reportdataStartDate = vCurr.fetchall()
    
    lst = []
    for x in sorted(reportdataStartDate, reverse=True):
        lst.append(datetime.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))
    
    # close connection.
    vCurr.close()
    
    # cleanup variables.
    del vCurr, vConn, reportdataStartDate
        
    return lst




'''
    Requirements:
    pacman -S firefox geckodriver
    pip install selenium
    pip install pandas
    
    Requirements:
    ! pacman -S firefox geckodriver
    ! pip install selenium
    ! pip install pandas
    ! pip install datetime
'''

# local modules
import urlParse

# PIP modules
import os
import glob
import sys
import json
import time
from datetime import datetime
import psycopg # SQL query
import pandas as pd

# Webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By




def SalesReport_to_SQL(*vURL, vSite, vUser, vPass, vServerDB, 
                                                   vServerUser, 
                                                   vServerPass, 
                                                   vServerIP, 
                                                   vServerPort):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        
            quickly added:
            vServerDB, 
            vServerUser, 
            vServerPass, 
            vServerIP, 
            vServerPort
    ''' 
        
    for file in glob.glob("/tmp/Sales Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # Geckodriver is required to make Selenium work.
    # possible do a find / | grep geckodriver and select the first path?
    s = Service('/usr/bin/geckodriver') 
    
    options = Options()
    # Speed up load times by disabling options
    options.set_preference("browser.tab.animate", 0)
    options.set_preference("browser.panorama.animate_zoom", 0)
    options.set_preference(" network.dns.disablePrefetch", True)
    options.set_preference("network.prefetch-next ", False)
    options.set_preference("network.http.speculative-parallel-limit", 0)
    options.set_preference("permissions.default.image", 2)
    options.set_preference("extensions.contentblocker.enabled", True)     
    #options.set_preference("javascript.enabled", False)
    options.set_preference("permissions.default.stylesheet", 2)
    
    # To prevent download dialog
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", "/tmp")
    #Example:profile.set_preference("browser.download.dir", "C:\Tutorial\down")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    
    options.headless = True # headless browser running option (Critical option)
    driver = webdriver.Firefox(service=s, options=options)  # load settings into firefox browser.
    
    ''' Login to Webpage
    '''
    
    # MAIN PAGE URL TO LOGIN
    driver.get('https://my.paypoint.com/login')
    
    # change to a wait for item on page with timeout.
    time.sleep(10)
    
    # 'PayPoint Retailer Portal' = logged out.
    # 'PayPoint EPoS' = logged in.
    if driver.title == 'PayPoint Retailer Portal':
        #print("Login Screen.")
        # INPUT PASSWORD
        driver.find_element(By.ID, "siteid_email").send_keys(vSite)
        driver.find_element(By.ID, "username").send_keys(vUser)
        driver.find_element(By.ID, "password").send_keys(vPass)
        driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    else:
        #print("Logged in.")
        pass
    
    # change to a wait for tile on page with timeout.
    time.sleep(5)
    
    # validation check
    if driver.title != 'PayPoint Retailer Portal':
        #driver.save_screenshot('ERROR_001.png')
        sys.exit("ERROR: 001 Still on Login Screen. " + driver.title)
    else:
        print("Logged in.")
    
    # connect to SQL
    ''' Connect to Databasse
    '''
    
    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB, 
                            user=vServerUser, 
                            password=vServerPass, 
                            host=vServerIP, 
                            port=vServerPort)

    # set the autocommit behavior of the current session.
    vConn.autocommit = True

    # Open a cursor to proform database operations.
    vCurr = vConn.cursor()
    
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        #checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    ''' Loop through vURL
    '''
    
    # loop through each instance.
    for u in vURL:        
        
        j = json.loads(urlDecode(str(u.split('=')[1])))
        # timestampStart_timestamp_end_saleType
        vStartDate = j[1]['data']['startDate']
        vEndDate   = j[1]['data']['endDate']
        vSaleType  = j[1]['name']
        print(vSaleType, 'on' , vStartDate, 'to', vEndDate, '- Loading.' )
        
        
        driver.get(u)
        #print("Loading " + u)
        
        # change to a wait for item on page with timeout.
        time.sleep(10)
        
        # Select Export dropdown
        driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
        print(vSaleType, 'on' , vStartDate, 'to', vEndDate, "- Selecting Export Dropdown.")
        # change to a wait for item on page with timeout.
        time.sleep(10)
        
        # Select Export button
        driver.find_element(By.LINK_TEXT, "Export to CSV").click()
        print(vSaleType, 'on' , vStartDate, 'to', vEndDate, "- Selecting Export Button.")

        # wait for file to appear.
        time.sleep(15)
        
        # local temp file path.
        vFile = '/tmp/Sales Report.csv'
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=False)
        
        # removes the temp report.
        os.remove(vFile)
        
        # adds startDate to data.
        try:
            csvData.insert(0,'startDate',vStartDate)
        except:
            pass
        
        # adds endDate to data.
        try:
            csvData.insert(1,'endDate',vEndDate)
        except:
            pass       
        
        # adds saleType to data.
        try:
            csvData.insert(2,'SaleType',vSaleType)
        except:
            pass
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)
        #return dataframe      
        
        
        # PRocess Fille to SQL
        for i in dataframe.index:
            
            #sorting out the barcode issue.
            vRawBardcode = dataframe[' Barcode'].fillna(0)[i]
            
            # checks if sting
            if isinstance(vRawBardcode, str):
                #checks if all digits
                if vRawBardcode.isdigit():
                    vBarcode = float(vRawBardcode)
                else:
                    vBarcode = '0.0'
            # checks digits
            elif isinstance(vRawBardcode, int):
                vBarcode = vRawBardcode
            elif isinstance(vRawBardcode,float):
                vBarcode = vRawBardcode
            else:
                vBarcode = '0.0'
            
            insert_table_query = '''insert into REPORTDATA (
                Category,
                startDate,
                endDate,
                SaleType,
                Item_Code,
                Description,
                Unit_Size,
                Barcode,
                Weighted_Qty,
                VATRate,
                Total_Qty,
                Total_Cost_Price,
                Total_Sales,
                Total_VAT,
                Avg_Margin,
                Total_Profit
               ) 
               values(
               '%s', '%s', '%s', '%s', '%s', 
               '%s', '%s', '%s', '%s', '%s', 
               '%s', '%s', '%s', '%s', '%s', 
               '%s'
               ); ''' % (
                        dataframe['Category'][i], 
                        datetime.strptime(dataframe['startDate'][i], "%d/%m/%Y %H:%M:%S"), 
                        datetime.strptime(dataframe['endDate'][i], "%d/%m/%Y %H:%M:%S"), 
                        dataframe['SaleType'][i], 
                        dataframe['Item Code'][i],
                        dataframe['Description'][i].replace("'",''), 
                        dataframe['Unit Size'][i],
                        vBarcode,
                        dataframe['Weighted Qty'][i], 
                        dataframe[' VAT  Rate'][i],
                        dataframe['Total Qty'][i], 
                        dataframe['Total Cost Price'][i],
                        dataframe['Total Sales'][i], 
                        dataframe['Total VAT'][i],
                        dataframe['Avg Margin'][i],
                        dataframe['Total Profit'][i]
                     )
            # sends query to SQL.
            vCurr.execute(insert_table_query)
            
            # Add verification step?
    vCurr.close() # Closing SQL Query
    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.




def TenderReport_to_SQL(*vURL, vSite, vUser, vPass, vServerDB, 
                                                   vServerUser, 
                                                   vServerPass, 
                                                   vServerIP, 
                                                   vServerPort):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        
            quickly added:
            vServerDB, 
            vServerUser, 
            vServerPass, 
            vServerIP, 
            vServerPort
    ''' 

    for file in glob.glob("/tmp/Tender Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # Geckodriver is required to make Selenium work.
    # possible do a find / | grep geckodriver and select the first path?
    s = Service('/usr/bin/geckodriver') 
    
    options = Options()
    # Speed up load times by disabling options
    options.set_preference("browser.tab.animate", 0)
    options.set_preference("browser.panorama.animate_zoom", 0)
    options.set_preference(" network.dns.disablePrefetch", True)
    options.set_preference("network.prefetch-next ", False)
    options.set_preference("network.http.speculative-parallel-limit", 0)
    options.set_preference("permissions.default.image", 2)
    options.set_preference("extensions.contentblocker.enabled", True)     
    #options.set_preference("javascript.enabled", False)
    options.set_preference("permissions.default.stylesheet", 2)
    
    # To prevent download dialog
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", "/tmp")
    #Example:profile.set_preference("browser.download.dir", "C:\Tutorial\down")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    
    options.headless = True # headless browser running option (Critical option)
    driver = webdriver.Firefox(service=s, options=options)  # load settings into firefox browser.
    
    ''' Login to Webpage
    '''

    # MAIN PAGE URL TO LOGIN.
    driver.get('https://my.paypoint.com/login')
    
    # change to a wait for item on page with timeout.
    time.sleep(10)
    
    # 'PayPoint Retailer Portal' = logged out.
    # 'PayPoint EPoS' = logged in.
    if driver.title == 'PayPoint Retailer Portal':
        #print("Login Screen.")
        # INPUT PASSWORD
        driver.find_element(By.ID, "siteid_email").send_keys(vSite)
        driver.find_element(By.ID, "username").send_keys(vUser)
        driver.find_element(By.ID, "password").send_keys(vPass)
        driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    else:
        #print("Logged in.")
        pass
    
    # change to a wait for tile on page with timeout.
    time.sleep(5)
    
    # validation check
    if driver.title != 'PayPoint Retailer Portal':
        #driver.save_screenshot('ERROR_001.png')
        sys.exit("ERROR: 001 Still on Login Screen. " + driver.title)
    else:
        print("Logged in.")
    
    
    # connect to SQL
    ''' Connect to Databasse
    '''

    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB, 
                            user=vServerUser, 
                            password=vServerPass, 
                            host=vServerIP, 
                            port=vServerPort)

    # set the autocommit behavior of the current session.
    vConn.autocommit = True

    # Open a cursor to proform database operations.
    vCurr = vConn.cursor()
    
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        #checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    ''' Loop through vURL
    '''
    
    # loop through each instance.
    for u in vURL:        
        
        j = json.loads(urlDecode(str(u.split('=')[1])))
        # timestampStart_timestamp_end_saleType
        vstartDate = j[1]['data']['startDate']
        vendDate = j[1]['data']['endDate']
        vPaymentMethod  = j[1]['name']
        print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, '- Loading.')
    
        
        driver.get(u)
        #print("Loading " + u)
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export dropdown
        driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
        print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export button
        driver.find_element(By.LINK_TEXT, "Export to CSV").click()
        print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

        # wait for file to apear.
        time.sleep(10)
        
        # local temp file path.
        vFile = '/tmp/Tender Report.csv'
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=False)
        
        # removes the temp report.
        os.remove(vFile)
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)    

        # Process File to SQL
        for i in dataframe.index:
            
            # Converting positive change into negative value.
            if dataframe['Description'][i] == 'Change Due' and dataframe['Amount'][i] > 0: 
                vAmount = dataframe['Amount'][i] * -1
            else: 
                vAmount = dataframe['Amount'][i]           
        
    
            insert_table_query = '''insert into TENDERDATA (
                datetime,
                paymentmethod,
                quantity,
                amount
               ) 
               values(
               '%s', '%s', '%s', '%s'
               ); ''' % (
                        dataframe['Date Time'][i],
                        dataframe['Description'][i].replace("'",''), 
                        dataframe['Qty'][i], 
                        vAmount
                     )
            
            # sends query to SQL.
            vCurr.execute(insert_table_query)
            
            
            # Add verification step?
    vCurr.close() # Closing SQL Query
    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.



def PPID_Report_to_SQL(*vURL, vSite, vUser, vPass, vServerDB, 
                                                   vServerUser, 
                                                   vServerPass, 
                                                   vServerIP, 
                                                   vServerPort):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        
            quickly added:
            vServerDB, 
            vServerUser, 
            vServerPass, 
            vServerIP, 
            vServerPort
    ''' 
        
    for file in glob.glob("/tmp/Tender Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # Geckodriver is required to make Selenium work.
    # possible do a find / | grep geckodriver and select the first path?
    s = Service('/usr/bin/geckodriver') 
    
    options = Options()
    # Speed up load times by disabling options
    options.set_preference("browser.tab.animate", 0)
    options.set_preference("browser.panorama.animate_zoom", 0)
    options.set_preference(" network.dns.disablePrefetch", True)
    options.set_preference("network.prefetch-next ", False)
    options.set_preference("network.http.speculative-parallel-limit", 0)
    options.set_preference("permissions.default.image", 2)
    options.set_preference("extensions.contentblocker.enabled", True)     
    #options.set_preference("javascript.enabled", False)
    options.set_preference("permissions.default.stylesheet", 2)
    
    # To prevent download dialog
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", "/tmp")
    #Example:profile.set_preference("browser.download.dir", "C:\Tutorial\down")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    
    options.headless = True # headless browser running option (Critical option)
    driver = webdriver.Firefox(service=s, options=options)  # load settings into firefox browser.
    
    ''' Login to Webpage
    '''
    
    # MAIN PAGE URL TO LOGIN.
    driver.get('https://my.paypoint.com/login')
    
    # change to a wait for item on page with timeout.
    time.sleep(10)
    
    # 'PayPoint Retailer Portal' = logged out.
    # 'PayPoint EPoS' = logged in.
    if driver.title == 'PayPoint Retailer Portal':
        #print("Login Screen.")
        # INPUT PASSWORD
        driver.find_element(By.ID, "siteid_email").send_keys(vSite)
        driver.find_element(By.ID, "username").send_keys(vUser)
        driver.find_element(By.ID, "password").send_keys(vPass)
        driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    else:
        #print("Logged in.")
        pass
    
    # change to a wait for tile on page with timeout.
    time.sleep(5)
    
    # validation check
    if driver.title != 'PayPoint Retailer Portal':
        #driver.save_screenshot('ERROR_001.png')
        sys.exit("ERROR: 001 Still on Login Screen. " + driver.title)
    else:
        print("Logged in.")
    
    
    # connect to SQL
    ''' Connect to Databasse
    '''

    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB, 
                            user=vServerUser, 
                            password=vServerPass, 
                            host=vServerIP, 
                            port=vServerPort)

    # set the autocommit behavior of the current session.
    vConn.autocommit = True

    # Open a cursor to proform database operations.
    vCurr = vConn.cursor()
    
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        #checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    ''' Loop through vURL
    '''
    
    # loop through each instance.
    for u in vURL:        
        
        j = json.loads(urlDecode(str(u.split('=')[1])))
        # timestampStart_timestamp_end_saleType
        vstartDate = j[0]['data']['startDate']
        vendDate = j[0]['data']['endDate']
        vPaymentMethod  = 'PPID'
        print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, '- Loading.')
    
        
        driver.get(u)
        #print("Loading " + u)
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export dropdown
        driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
        print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export button
        driver.find_element(By.LINK_TEXT, "Export to CSV").click()
        print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

        # wait for file to apear.
        time.sleep(10)
        
        # local temp file path.
        vFile = '/tmp/Pay Point Report.csv'
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=False)
        
        # removes the temp report.
        os.remove(vFile)
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)
        
        # Process File to SQL
        for i in dataframe.index:
    
            insert_table_query = '''insert into PPIDDATA (
                date_time,
                employee,
                scheme_name,
                scheme_group,
                id,
                sale_type,
                amount
               ) 
               values(
               '%s', '%s', '%s', '%s', '%s',
               '%s', '%s'
               ); ''' % (
                        dataframe['Time'][i],
                        dataframe['User'][i],
                        dataframe['Scheme Name'][i].rstrip(),
                        dataframe['Scheme Group'][i],
                        dataframe[' Txn  Id'][i],
                        dataframe['Txn Type'][i],
                        dataframe['Amount'][i]
                        )
            
            # sends query to SQL.
            vCurr.execute(insert_table_query)
            
            
            # Add verification step?
    vCurr.close() # Closing SQL Query
    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.