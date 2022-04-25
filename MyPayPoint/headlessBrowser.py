import urlParse

def DownloadSalesReport_to_CSV(*vURL, vSite, vUser, vPass,vPath):
    '''
        Requirements:
        pacman -S firefox geckodriver
        pip install selenium
        pip install pandas
        
        
        DownloadReport(vURL, vSite=vSite, vUser=vUser, vPass=vPass,vPath=vPath),
        
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    import os
    import glob
    import sys
    import json
    import time
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    
    ''' Prep 
    '''    
    
    #checks if path ends with a slash
    if not vPath.endswith('/'):
        vPath = vPath + '/'
    
    for file in glob.glob("/tmp/Sales Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # need a better way of findiner it
    vGeckodriver = '/usr/bin/geckodriver'
    s = Service(vGeckodriver) # service object for 
    
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
    # headless running
    options.headless = True
    driver = webdriver.Firefox(service=s, options=options) 
    
    
    ''' Login to Webpage
    '''
    
    vURLlogin = 'https://my.paypoint.com/login'
    # MAIN PAGE URL TO LOGIN
    driver.get(vURLlogin)
    
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

    def urlDecode(vURLQuery):
        import urllib.parse 
        return (urllib.parse.unquote_to_bytes(urllib.parse.unquote_plus(vURLQuery))).decode('utf-8')


        
    # converts turple into list.
    if not isinstance(vURL, list):
        vURL = list(vURL)
        
        #checks if list, is nested in a list.
        if not isinstance(vURL[0],str):
            vURL = vURL[0]
    
    # loop through each instance.
    for u in vURL:        
        
        j = json.loads(urlDecode(str(u.split('=')[1])))
        # timestampStart_timestamp_end_saleType
        vStartDate = j[1]['data']['startDate']
        vEndDate   = j[1]['data']['endDate']
        vSaleType  = j[1]['name']
        print(vSaleType, 'on', vStartDate, 'to', vEndDate, '- Loading.' )
        
        
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
        
        #,vPath
        import pandas as pd
        # local temp file path.
        vFile = '/tmp/Sales Report.csv'
        
        # loads csv into memory.
        csvData=pd.read_csv(vFile,
                         encoding='latin1',
                         header=1,
                         index_col=0)
        
        # removes the temp report.
        os.remove(vFile)
        
        # adds startDate to data.
        try:
            csvData.insert(0,'startDate',vStartDate)
        except:
            pass
        
        # adds endDate to data.
        try:
            csvData.insert(1,'endDate',vStartDate)
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
        vFileName = vStartDate.replace('/','').replace(':','').replace(' ','') + '_' + vEndDate.replace('/','').replace(':','').replace(' ','') + '_' + vSaleType.replace(' ','_') + '.csv'
        vOutput = vPath + vFileName
        dataframe.to_csv(vOutput)
        
        #cleanup
        del vOutput
        del dataframe
        
        

def DownloadSalesReport_to_SQL(*vURL, vSite, vUser, vPass):
    '''
        Requirements:
        !pacman -S firefox geckodriver
        !pip install selenium
        !pip install pandas
        !pip install sqlalchemy
        ! pip install datetime
        
        DownloadReport(vURL, vSite=vSite, vUser=vUser, vPass=vPass,vPath=vPath),
        
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    import os
    import glob
    import sys
    import json
    import time
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    import psycopg
    
    ''' Prep 
    '''    
        
    for file in glob.glob("/tmp/Sales Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # need a better way of findiner it
    vGeckodriver = '/usr/bin/geckodriver'
    s = Service(vGeckodriver) # service object for 
    
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
    # headless running
    options.headless = True
    driver = webdriver.Firefox(service=s, options=options) 
    
    
    ''' Login to Webpage
    '''
    
    vURLlogin = 'https://my.paypoint.com/login'
    # MAIN PAGE URL TO LOGIN
    driver.get(vURLlogin)
    
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
    

    def urlDecode(vURLQuery):
        import urllib.parse 
        return (urllib.parse.unquote_to_bytes(urllib.parse.unquote_plus(vURLQuery))).decode('utf-8')
    
    #Temp variabls
    ''' SQL Variables (to be removed into input)
    '''

    # Variables used while testing.
    vServerIP   = ''
    vServerPort = ''
    vServerDB   = ''
    vServerUser = ''
    vServerPass = ''
    
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

        # wait for file to apear.
        time.sleep(15)
        
        #,vPath
        import pandas as pd
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



def DownloadTenderReport_to_SQL(*vURL, vSite, vUser, vPass):
    '''
        Requirements:
        !pacman -S firefox geckodriver
        !pip install selenium
        !pip install pandas
        !pip install sqlalchemy
        ! pip install datetime
        
        DownloadReport(vURL, vSite=vSite, vUser=vUser, vPass=vPass,vPath=vPath),
        
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    import os
    import glob
    import sys
    import json
    import time
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    import psycopg
    
    '''
        Prep 
    '''    
        
    for file in glob.glob("/tmp/Tender Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # need a better way of findiner it
    vGeckodriver = '/usr/bin/geckodriver'
    s = Service(vGeckodriver) # service object for 
    
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
    # headless running
    options.headless = True
    driver = webdriver.Firefox(service=s, options=options) 
    
    
    ''' Login to Webpage
    '''
    
    vURLlogin = 'https://my.paypoint.com/login'
    # MAIN PAGE URL TO LOGIN
    driver.get(vURLlogin)
    
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
    

    def urlDecode(vURLQuery):
        import urllib.parse 
        return (urllib.parse.unquote_to_bytes(urllib.parse.unquote_plus(vURLQuery))).decode('utf-8')
    
    #Temp variabls
    ''' SQL Variables (to be removed into input)
    '''
    
    # Variables used while testing.
    vServerIP   = ''
    vServerPort = ''
    vServerDB   = ''
    vServerUser = ''
    vServerPass = ''
    
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
        
        #,vPath
        import pandas as pd
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
        
        #return dataframe      
        
        
        ''' Section to change for tender report
        
            - Need to check what the columns are.
                - Work out what type each column is. Should be simple, run report for a duration for template data.
            - Is there any data that can cause any issues on run? 
                - Create some trial run data 
                - Select correct database.
        '''
        

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



def DownloadPPIDReport_to_SQL(*vURL, vSite, vUser, vPass):
    '''
        Requirements:
        !pacman -S firefox geckodriver
        !pip install selenium
        !pip install pandas
        !pip install sqlalchemy
        ! pip install datetime
        
        DownloadReport(vURL, vSite=vSite, vUser=vUser, vPass=vPass,vPath=vPath),
        
        Arguments:
        vURL : URL of Paypoint
        vSite: Site Code
        vUser: username
        vPass: password
        vPath: Path of output /export/
    ''' 
    
    import os
    import glob
    import sys
    import json
    import time
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from selenium.webdriver.common.by import By
    import psycopg
    
    '''
        Prep 
    '''    
        
    for file in glob.glob("/tmp/Tender Report*"):
        try:
            os.remove(file)
        except:
            print('Error while deleting file : ', file)    
    
    ''' Start Session 
    '''
    
    # need a better way of findiner it
    vGeckodriver = '/usr/bin/geckodriver'
    s = Service(vGeckodriver) # service object for 
    
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
    # headless running
    options.headless = True
    driver = webdriver.Firefox(service=s, options=options) 
    
    
    ''' Login to Webpage
    '''
    
    vURLlogin = 'https://my.paypoint.com/login'
    # MAIN PAGE URL TO LOGIN
    driver.get(vURLlogin)
    
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
    

    def urlDecode(vURLQuery):
        import urllib.parse 
        return (urllib.parse.unquote_to_bytes(urllib.parse.unquote_plus(vURLQuery))).decode('utf-8')
    
    #Temp variabls
    ''' SQL Variables (to be removed into input)
    '''
    
    # Variables used while testing.
    vServerIP   = ''
    vServerPort = ''
    vServerDB   = ''
    vServerUser = ''
    vServerPass = ''
    
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
        
        #,vPath
        import pandas as pd
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