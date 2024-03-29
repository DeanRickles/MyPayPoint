'''
    Requirements:
    pacman -S firefox geckodriver
    pip install selenium, pandas, datetime
'''

# local modules
from . import urlParse


import re # required for regex with receipts.
import os
import glob
import sys
import json
import time
#from datetime import datetime
#import psycopg # SQL query
import pandas as pd

# Webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


def SalesReport_to_CSV(*vURL, vSite, vUser, vPass, vPath):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    #checks if path ends with a slash
    if not vPath.endswith('/'):
        vPath = vPath + '/'
    
    # checks to find file in expected location and removes any.
    for file in glob.glob("/tmp/Sales Report*"): #Diff
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
        print("SALESREPORT: Logged in.")
    
    
    ''' Loop file download here.
    '''
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        # checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    # loop through each URL instance.
    for u in vURL:        
        
        # parse url breadcrumbs.
        j = json.loads(urlParse.urlDecode(str(u.split('=')[1])))
        # timestampStart_timestamp_end_saleType
        vStartDate = j[1]['data']['startDate']
        vEndDate   = j[1]['data']['endDate']
        vSaleType  = j[1]['name'] #Diff
        del j # clear json after load.
        
        print(vSaleType, 'on', vStartDate, 'to', vEndDate, '- Loading.' )
        
        # Loads current instance URL into webdriver.
        driver.get(u)
        #print("Loading " + u)
        
        # change to a wait for item on page with timeout.
        time.sleep(10)
        
        # Select Export dropdown
        driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
        print(vSaleType, 'on', vStartDate, 'to', vEndDate, "- Selecting Export Dropdown.")
        
        # change to a wait for item on page with timeout.
        time.sleep(10)
        
        # Select Export button
        driver.find_element(By.LINK_TEXT, "Export to CSV").click()
        print(vSaleType, 'on', vStartDate, 'to', vEndDate, "- Selecting Export Button.")

        # wait for file to apear.
        time.sleep(15)
        
        # expected local temp file path.
        vFile = '/tmp/Sales Report.csv' #Diff
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=0)
        
        # removes the temp report.
        os.remove(vFile)
        
        # adds startDate to data.
        try:
            csvData.insert(0,'datetime',vStartDate)
        except:
            pass
        
        # adds endDate to data.
        try:
            csvData.insert(1,'enddatetime',vStartDate)
        except:
            pass       
        
        # adds saleType to data.
        try:
            csvData.insert(2,'SaleType',vSaleType)
        except:
            pass
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)
        
        # export data to vPath.
        # formart startdate_enddate_saletype.csv
        vFileName = vStartDate.replace('/','').replace(':','').replace(' ','') + '_' + vEndDate.replace('/','').replace(':','').replace(' ','') + '_' + vSaleType.replace(' ','_') + '.csv'
        
        # export path fullname
        vFullName = vPath + vFileName
        
        # export dataframe into csv format.
        dataframe.to_csv(vFullName,
                         index=False)
        
        # Return the file for passthrough
        return vFullName
        
        # Clean-up variables
        del dataframe

        
def TenderReport_to_CSV(*vURL, vSite, vUser, vPass, vPath):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    #checks if path ends with a slash
    if not vPath.endswith('/'):
        vPath = vPath + '/'
    
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
        vendDate   = j[1]['data']['endDate']
        vPaymentMethod  = j[1]['name'] #Diff
        
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
        vFile = '/tmp/Tender Report.csv' #Diff
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=False)
        
        # removes the temp report.
        os.remove(vFile)
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData) 
        # adds startDate to data.
        try:
            csvData.insert(0,'datetime',vstartDate)
        except:
            pass
        
        # adds endDate to data.
        try:
            csvData.insert(1,'enddatetime',vendDate)
        except:
            pass       
        
        # adds saleType to data.
        try:
            csvData.insert(2,'SaleType',vPaymentMethod) #Diff
        except:
            pass
        
        # convert data into exportable format.
        #dataframe = pd.DataFrame(csvData)
        
        # export data to vPath.
        # formart startdate_enddate_saletype.csv
        vFileName = vstartDate.replace('/','').replace(':','').replace(' ','') + '_' + vendDate.replace('/','').replace(':','').replace(' ','') + '_' + vPaymentMethod.replace(' ','_') + '.csv'
        
        # export path fullname
        vFullName = vPath + vFileName
        
        # export dataframe into csv format.
        dataframe.to_csv(vFullName,
                         index=False)
        
        # Return the file for passthrough
        return vFullName
        
        # Clean-up variables
        del dataframe



def PPIDReport_to_CSV(*vURL, vSite, vUser, vPass, vPath):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    #checks if path ends with a slash
    if not vPath.endswith('/'):
        vPath = vPath + '/'
    
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
    
    
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        #checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    ''' Loop through vURL
    '''
    
    # used to output files created.
    vOutput = []
    
    # loop through each instance.
    for u in vURL:        
        
        j = json.loads(urlParse.urlDecode(str(u.split('=')[1])))
        # timestampStart_timestamp_end_saleType
        vstartDate = j[0]['data']['startDate']
        vendDate = j[0]['data']['endDate']
        vSaleType  = 'PPID' #Diff
        
        print(vSaleType, 'on', vstartDate, 'to', vendDate, '- Loading.')
        
        driver.get(u)
        #print("Loading " + u)
        
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export dropdown
        driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
        print(vSaleType, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export button
        driver.find_element(By.LINK_TEXT, "Export to CSV").click()
        print(vSaleType, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

        # wait for file to apear.
        time.sleep(10)
        
        # local temp file path.
        vFile = '/tmp/Pay Point Report.csv' #Diff
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=False)
        
        # removes the temp report.
        os.remove(vFile)
        
        # convert data into exportable format.
        #dataframe = pd.DataFrame(csvData)
        
        # adds startDate to data.
        try:
            csvData.insert(0,'datetime',vstartDate)
        except:
            pass
        
        # adds endDate to data.
        try:
            csvData.insert(1,'enddatetime',vendDate)
        except:
            pass       
        
        # adds saleType to data.
        try:
            csvData.insert(2,'SaleType',vSaleType)
        except:
            pass
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)
        
        # export data to vPath.
        # formart startdate_enddate_saletype.csv
        vFileName = vstartDate.replace('/','').replace(':','').replace(' ','') + '_' + vendDate.replace('/','').replace(':','').replace(' ','') + '_' + vSaleType.replace(' ','_') + '.csv'
        
        # export path fullname
        vFullName = vPath + vFileName
        
        # export dataframe into csv format.
        dataframe.to_csv(vFullName,
                         index=False)
        
        
        # pass vFullName into list for reutrn at end.
        # Return the file for passthrough
        vOutput.append(vFullName)
        
    # Clean-up variables
    del dataframe, vFullName, vPath, vFileName, csvData, vFile
    
    # output the list of files created.
    return vOutput



def ReceiptReport_to_CSV(*vURL, vSite, vUser, vPass, vPath):
    '''
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    #checks if path ends with a slash
    if not vPath.endswith('/'):
        vPath = vPath + '/'
    
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
    
    
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        #checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    ''' Loop through vURL
    '''
    
    # used to output files created.
    vOutput = []
    
    # loop through each instance.
    for u in vURL:        

        # use regex to parse the datetime and enddatetime from the URL. Requires re module.
        # timestampStart_timestamp_end_saleType
        vstartDate = datetime.strftime(datetime.strptime(re.search("startDateTime=(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", u)[1],'%Y-%m-%d-%H-%M-%S'),'%Y/%m/%d %H:%M:%S')
        vendDate   = datetime.strftime(datetime.strptime(re.search("endDateTime=(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})", u)[1],'%Y-%m-%d-%H-%M-%S'),'%Y/%m/%d %H:%M:%S')
        vSaleType  = 'Receipt' #Diff
        
        print(vSaleType, 'on', vstartDate, 'to', vendDate, '- Loading.')
        
        driver.get(u)
        #print("Loading " + u)
        
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export dropdown
        driver.find_element(By.CSS_SELECTOR, ".btn-group:nth-child(1) > .btn").click()
        print(vSaleType, 'on', vstartDate, 'to', vendDate, "- Selecting Export Dropdown.")
        # change to a wait for item on page with timeout.
        time.sleep(5)
        
        # Select Export button
        driver.find_element(By.LINK_TEXT, "Export to CSV").click()
        print(vSaleType, 'on', vstartDate, 'to', vendDate, "- Selecting Export Button.")

        # wait for file to apear.
        time.sleep(10)
        
        # local temp file path.
        vFile = '/tmp/ReceiptViewerReport.csv' #Diff
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=False)
        
        # removes the temp report.
        os.remove(vFile)
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)
        
        # adds startDate to data.
        #try:
        #    csvData.insert(0,'datetime',vstartDate)
        #except:
        #    pass
        
        # adds endDate to data.
        #try:
        #    csvData.insert(1,'enddatetime',vendDate)
        #except:
        #    pass       
        
        # adds saleType to data.
        try:
            csvData.insert(3,'SaleType',vSaleType)
        except:
            pass
        
        # convert data into exportable format.
        dataframe = pd.DataFrame(csvData)
        
        # export data to vPath.
        # formart startdate_enddate_saletype.csv
        vFileName = vstartDate.replace('/','').replace(':','').replace(' ','') + '_' + vendDate.replace('/','').replace(':','').replace(' ','') + '_' + vSaleType.replace(' ','_') + '.csv'
        
        # export path fullname
        vFullName = vPath + vFileName
        
        # export dataframe into csv format.
        dataframe.to_csv(vFullName,
                         index=False)
        
        
        # pass vFullName into list for reutrn at end.
        # Return the file for passthrough
        vOutput.append(vFullName)
        
    # Clean-up variables
    del dataframe, vFullName, vPath, vFileName, csvData, vFile
    
    # output the list of files created.
    return vOutput