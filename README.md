### MyPayPoint

Python script to scrape https://my.paypoint.com reports of the webiste and into Postgress.

Script is broken into modules and can be altered to suit the user.

## To Do:
This section is purely to help me keep on track and note what needs to be done.

Starting with Sales and then add each catagory type after.

Key:
```diff
+ = Completed  [Timestamp](Comment)
! = On-hold    [Timestamp](Reason)
x = Scrapped   [Timestamp](Reason)
~ = Re-writing [Timestamp](Comment)
```

General:
```diff
- Scope out all varaibles and remove any unrequired.
- Move main varaibles into .env
- PIP requirement file.
- Standardise datetime header
- Move SQL qeruies own module.
```

# Module

datePeriod.py
```diff
+ compareDateList [24/04/2022]()
+ dateSplan       [24/04/2022]()
+ filterWorkDay   [24/04/2022](Requires re-writing.)
+ reportHourlyEnd [24/04/2022](Rename Function.)
```

urlParse.py
```diff
+ (URL parse) Decode. [24/04/2022]()
+ (URL parse) Encode. [24/04/2022]()
```

generateUrl.py
```diff
generateURL
    1) using  selected inputs manulate a URL for downloadrReport.
- (Sales) generateURL
- (Tender) generateURL
- (PPID) generateURL
- (Recepts) generateURL
```

downloadReport.py
```diff
Scrape CSV File.
        1) Open webbrowser
        2) Download report based on URL.
        3) Return list of file paths.
- (Sales)    Scrape CSV File. [24/04/2022](Need to re-write to be generalised for import.)
- (Tender)   Scrape CSV File. 
- (PPID)     Scrape CSV File. 
- (Recepts)  Scrape CSV File. 
```

sqlQueries.py (postgres)
```diff
Distinct Dates
    1) Open SQL connection.
    2) Read distinct dates the stored SQL.
    3) Return date list.
- (Sales)    Get Distinct Dates in SQL. [24/04/2022](Requires re-writing) 
- (Tender)   Get Distinct Dates in SQL. [24/04/2022](Requires re-writing)
- (PPID)     Get Distinct Dates in SQL.
- (Reciepts) Get Distinct Dates in SQL.
```
```diff
Import CSV to SQL
    1) Convert CSV into table.
    2) Open SQL connection.
    3) insert Table into SQL.
- (Sales)    Import CSV into SQL.
- (Tender)   Import CSV into SQL.
- (PPID)     Import CSV into SQL.
- (Recepts)  Import CSV into SQL.
```