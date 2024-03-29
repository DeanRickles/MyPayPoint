# local modules
from . import urlParse

# PIP modules
import os
import re
import glob
import sys
import json
import time
import psycopg # SQL query
import pandas as pd
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

# wait for item.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def GetDateTime(vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
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

    with vConn:
        # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:

            # execute command
            vCurr.execute(f'''SELECT DISTINCT datetime
                        from public.{vServerTbl};''')

            # fetch mutli line
            vDateTime = vCurr.fetchall()

            lst = []
            for x in sorted(vDateTime, reverse=True):
                lst.append(dt.strftime(x[0],  "%d/%m/%Y %H:%M:%S"))
    del vDateTime
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


def SalesReport_to_SQL(*vURL, vSite, vUser, vPass,
                       vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Setup for Postgres.

        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password

        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
    '''

    for file in glob.glob("/tmp/Sales Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)

    ''' Start Session
    '''

    # Geckodriver is required to make Selenium work.
    # possible do a find / | grep geckodriver and select the first path? Need to add error catch
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
    wait = WebDriverWait(driver, 60) # expected_conditions

    ''' Login to Webpage
    '''

    # MAIN PAGE URL TO LOGIN
    driver.get('https://my.paypoint.com/login')
    # wait for login page to load.
    element = wait.until(EC.visibility_of_element_located( (By.ID, "siteid_email")), "Login screen didn't load." )
    driver.find_element(By.ID, "siteid_email").send_keys(vSite)
    driver.find_element(By.ID, "username").send_keys(vUser)
    driver.find_element(By.ID, "password").send_keys(vPass)
    driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    # wait for login page to change load.
    element = wait.until(EC.invisibility_of_element_located( (By.ID, "siteid_email")), "Still on the login screen." )

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

    with vConn:
        # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:

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

                j = json.loads(urlParse.urlDecode(str(u.split('=')[1])))
                # timestampStart_timestampend_saleType
                vStartDate = j[1]['data']['startDate']
                vEndDate   = j[1]['data']['endDate']
                vSaleType  = j[1]['name']
                print(vSaleType, 'on' , vStartDate, 'to', vEndDate, '- Loading.' )

                #load url
                driver.get(u)

                # wait for export dropdown.
                element = wait.until(EC.visibility_of_element_located( (By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn")), "Unable to find Export dropdown." )
                # buffer on the load time. Loading too fast.
                time.sleep(5)
                # Select Export dropdown
                driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
                print(vSaleType, 'on' , vStartDate, 'to', vEndDate, "- Selecting Export Dropdown.")

                # wait for export button.
                element = wait.until(EC.visibility_of_element_located( (By.LINK_TEXT, "Export to CSV") ), "Unable to find Export button." )
                # Select Export button
                driver.find_element(By.LINK_TEXT, "Export to CSV").click()
                print(vSaleType, 'on' , vStartDate, 'to', vEndDate, "- Selecting Export Button.")

                # local temp file path.
                vFile = '/tmp/Sales Report.csv'
                # wait for file to appear.
                i = 0
                while not os.path.exists(vFile):
                    i += 1
                    time.sleep(1)
                    if i >=60:
                        sys.exit("ERROR: File Not found. "+ vFile)
                #buffer for the file to completely load.
                time.sleep(2)
                # loads csv into memory.
                csvData=pd.read_csv(vFile,
                                encoding='latin1',
                                header=1,
                                index_col=False)
                # removes the temp report.
                os.remove(vFile)

                # adds startDate to data.
                try:    csvData.insert(0,'datetime',vStartDate)
                except: pass
                # adds endDate to data.
                try:    csvData.insert(1,'enddatetime',vEndDate)
                except: pass
                # adds saleType to data.
                try:    csvData.insert(2,'SaleType',vSaleType)
                except: pass

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

                    insert_table_query = f'''insert into {vServerTbl} (
                        Category,
                        datetime,
                        enddatetime,
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
                                dt.strptime(dataframe['datetime'][i], "%d/%m/%Y %H:%M:%S"),
                                dt.strptime(dataframe['enddatetime'][i], "%d/%m/%Y %H:%M:%S"),
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
    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.




def TenderReport_to_SQL(*vURL, vSite, vUser, vPass,
                       vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Setup for Postgres.

        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password

        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
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
    wait = WebDriverWait(driver, 60) # expected_conditions

    ''' Login to Webpage
    '''

    # MAIN PAGE URL TO LOGIN
    driver.get('https://my.paypoint.com/login')
    # wait for login page to load.
    element = wait.until(EC.visibility_of_element_located( (By.ID, "siteid_email")), "Login screen didn't load." )
    driver.find_element(By.ID, "siteid_email").send_keys(vSite)
    driver.find_element(By.ID, "username").send_keys(vUser)
    driver.find_element(By.ID, "password").send_keys(vPass)
    driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    # wait for login page to change load.
    element = wait.until(EC.invisibility_of_element_located( (By.ID, "siteid_email")), "Still on the login screen." )

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

    with vConn:
        # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:

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

                j = json.loads(urlParse.urlDecode(str(u.split('=')[1])))
                # timestampStart_timestamp_end_saleType
                vstartDate = j[1]['data']['startDate']
                vendDate = j[1]['data']['endDate']
                vPaymentMethod  = j[1]['name']
                print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, '- Loading.')

                # Load url.
                driver.get(u)

                # wait for export dropdown.
                element = wait.until(EC.visibility_of_element_located( (By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn")), "Unable to find Export dropdown." )
                # buffer on the load time. Loading too fast.
                time.sleep(5)
                # Select Export dropdown
                driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
                print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")

                # wait for export button.
                element = wait.until(EC.visibility_of_element_located( (By.LINK_TEXT, "Export to CSV") ), "Unable to find Export button." )
                # Select Export button
                driver.find_element(By.LINK_TEXT, "Export to CSV").click()
                print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

                # local temp file path.
                vFile = '/tmp/Tender Report.csv'
                # wait for file to appear.
                i = 0
                while not os.path.exists(vFile):
                    i += 1
                    time.sleep(1)
                    if i >=60:
                        sys.exit("ERROR: File Not found. "+ vFile)
                #buffer for the file to completely load.
                time.sleep(2)
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

                    insert_table_query = f'''insert into {vServerTbl} (
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
    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.



def PPIDReport_to_SQL(*vURL, vSite, vUser, vPass,
                       vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Setup for Postgres.
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password

        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
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
    wait = WebDriverWait(driver, 60) # expected_conditions

    ''' Login to Webpage
    '''

    # MAIN PAGE URL TO LOGIN
    driver.get('https://my.paypoint.com/login')
    # wait for login page to load.
    element = wait.until(EC.visibility_of_element_located( (By.ID, "siteid_email")), "Login screen didn't load." )
    driver.find_element(By.ID, "siteid_email").send_keys(vSite)
    driver.find_element(By.ID, "username").send_keys(vUser)
    driver.find_element(By.ID, "password").send_keys(vPass)
    driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    # wait for login page to change load.
    element = wait.until(EC.invisibility_of_element_located( (By.ID, "siteid_email")), "Still on the login screen." )

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

    with vConn:
        # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:

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

                j = json.loads(urlParse.urlDecode(str(u.split('=')[1])))
                # timestampStart_timestamp_end_saleType
                vstartDate = j[0]['data']['startDate']
                vendDate = j[0]['data']['endDate']
                vPaymentMethod  = 'PPID'
                print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, '- Loading.')

                # load url.
                driver.get(u)

                # wait for export dropdown.
                element = wait.until(EC.visibility_of_element_located( (By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn")), "Unable to find Export dropdown." )
                # buffer on the load time. Loading too fast.
                time.sleep(5)
                # Select Export dropdown
                driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
                print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")

                # wait for export button.
                element = wait.until(EC.visibility_of_element_located( (By.LINK_TEXT, "Export to CSV") ), "Unable to find Export button." )
                # Select Export button
                driver.find_element(By.LINK_TEXT, "Export to CSV").click()
                print(vPaymentMethod, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

                # local temp file path.
                vFile = '/tmp/Pay Point Report.csv'
                # wait for file to appear.
                i = 0
                while not os.path.exists(vFile):
                    i += 1
                    time.sleep(1)
                    if i >=60:
                        sys.exit("ERROR: File Not found. "+ vFile)
                #buffer for the file to completely load.
                time.sleep(2)
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

                    insert_table_query = f'''insert into {vServerTbl} (
                        datetime,
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

    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.

def ReceiptsReport_to_SQL(*vURL, vSite, vUser, vPass,
                       vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Setup for Postgres.
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password

        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
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
    wait = WebDriverWait(driver, 60) # expected_conditions

    ''' Login to Webpage
    '''

    # MAIN PAGE URL TO LOGIN
    driver.get('https://my.paypoint.com/login')
    # wait for login page to load.
    element = wait.until(EC.visibility_of_element_located( (By.ID, "siteid_email")), "Login screen didn't load." )
    driver.find_element(By.ID, "siteid_email").send_keys(vSite)
    driver.find_element(By.ID, "username").send_keys(vUser)
    driver.find_element(By.ID, "password").send_keys(vPass)
    driver.find_element(By.CSS_SELECTOR, "#loginButton .pad-left").click()
    # wait for login page to change load.
    element = wait.until(EC.invisibility_of_element_located( (By.ID, "siteid_email")), "Still on the login screen." )

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

    with vConn:
        # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:

            # converts turple into list.
            if not isinstance(vURL, list):
                vURL = list(vURL)

                #checks if list, is nested in a list.
                if not isinstance(vURL[0],str):
                    vURL = vURL[0]

            ''' Loop through vURL
            '''

            # loop through each instance.
            for u in vURL:#

                # use regex to parse the datetime and enddatetime from the URL. Requires re module.
                # timestampStart_timestamp_end_saleType
                vstartDate = datetime.strftime(datetime.strptime(re.search("startDateTime=(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", u)[1],'%Y-%m-%d-%H-%M-%S'),'%Y/%m/%d %H:%M:%S')
                vendDate   = datetime.strftime(datetime.strptime(re.search("endDateTime=(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", u)[1],'%Y-%m-%d-%H-%M-%S'),'%Y/%m/%d %H:%M:%S')
                vSaleType  = 'Receipts'


                print(vSaleType, 'on', vstartDate, 'to', vendDate, '- Loading.')

                # load url.
                driver.get(u)

                # wait for export dropdown.
                element = wait.until(EC.visibility_of_element_located( (By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn")), "Unable to find Export dropdown." )
                # buffer on the load time. Loading too fast.
                time.sleep(5)
                # Select Export dropdown
                driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
                print(vSaleType, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")

                # wait for export button.
                element = wait.until(EC.visibility_of_element_located( (By.LINK_TEXT, "Export to CSV") ), "Unable to find Export button." )
                # Select Export button
                driver.find_element(By.LINK_TEXT, "Export to CSV").click()
                print(vSaleType, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

                # local temp file path.
                vFile = '/tmp/ReceiptViewerReport.csv'
                # wait for file to appear.
                i = 0
                while not os.path.exists(vFile):
                    i += 1
                    time.sleep(1)
                    if i >=60:
                        sys.exit("ERROR: File Not found. " + vFile)
                #buffer for the file to completely load.
                time.sleep(2)

                # loads csv into memory.
                csvData=pd.read_csv(vFile,
                                 encoding='latin1',
                                 header=1,
                                 index_col=False)

                # removes the temp report.
                os.remove(vFile)

                # adds saleType to data.
                try:
                    csvData.insert(3,'SaleType',vSaleType)
                except:
                    pass

                # convert data into exportable format.
                dataframe = pd.DataFrame(csvData)

                # Process File to SQL
                for i in dataframe.index:
                    insert_table_query = f'''insert into {vServerTbl} (
                        id,
                        ppid,
                        datetime,
                        saletype,
                        tid,
                        till_no,
                        "user",
                        net_value
                       )
                       values(
                       '%s', '%s', '%s', '%s', '%s',
                       '%s', '%s', '%s'
                       ); ''' % (
                                dataframe['ID'][i],
                                str(dataframe['PPID'][i]).replace('nan',''),
                                dataframe['Date'][i],
                                dataframe['SaleType'][i],
                                dataframe['Tid'][i],
                                str(dataframe['Till No.'][i]).replace('nan',''),
                                dataframe['User ID'][i],
                                dataframe['Net Value'][i]
                                )
                    # sends query to SQL.
                    vCurr.execute(insert_table_query)
    driver.close() # Closing Browser.
    driver.quit() # Quitting Browser.



def create_receipt_table(vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Requirement:
            pip install psycopg-binary psycopg

        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
    '''

    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB,
                            user=vServerUser,
                            password=vServerPass,
                            host=vServerIP,
                            port=vServerPort)

    # set the autocommit behavior of the current session.
    vConn.autocommit = True

    with vConn:
         # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:

            # Generate the insert query.
            create_table_query = f'''CREATE TABLE {vServerTbl} (
               id NUMERIC,
                ppid TEXT,
                datetime TIMESTAMP,
                saletype TEXT,
                tid NUMERIC,
                till_no TEXT,
                "user" TEXT,
                net_value NUMERIC
            ) '''

            vCurr.execute(create_table_query)

    # Close conection to the database.
    vConn.close()