# MyPayPoint

#### Introduction
Python script to scrape https://my.paypoint.com reports of the webiste and into Postgress.

Script is broken into modules and can be altered to suit the user.

---

#### To Do:
This section is purely to help me keep on track and note what needs to be done.

Starting with Sales and then add each catagory type after.


###### Bug fixes:
- [ ] Scope out all varaibles and remove any unrequired.
- [ ] Move main varaibles into .env
- [ ] Pacman requirement file.
- [ ] PIP requirement file.
- [ ] Standardise datetime header. datetime = StartDate && enddatetime = Enddate
    - [ ] checked datePeriod.py
    - [ ] checked downloadReport.py
    - [ ] checked generateURL.py
    - [ ] checked Report_to_sql.py
    - [ ] checked sql.py
- [ ] Move SQL queries to own module.
- [ ] Review variable notes in each function.
- [ ] Issue with barcodes not always importing

###### Module

###### datePeriod.py

- [x] compareDateList [24/04/2022] ()
- [x] dateSplan       [24/04/2022] ()
- [x] filterWorkDay   [24/04/2022] (Requires re-writing.)
- [x] reportHourlyEnd [24/04/2022] (Rename Function.)


###### urlParse.py
- [x] (URL parse) Decode. [24/04/2022] ()
- [x] (URL parse) Encode. [24/04/2022] ()


###### generateUrl.py

*Type*URL(vStartTimestamp,vEndTimeStamp,vPaymentMethod)

    1) using  selected inputs manulate a breadcrumb URL for downloadReport.

- [x] (Sales)   generateURL
- [x] (Tender)  generateURL
- [x] (PPID)    generateURL
- [ ] (Reciepts) generateURL
- [ ] Review option to consolidate functions into one. 


###### downloadReport.py

Scrape CSV File.

    1) Open webbrowser
    2) Download report based on URL.
    3) Return list of file paths.

- [x] (Sales)    Scrape CSV File.
    [24/04/2022] (Need to re-write to be generalised for import.)
- [x] (Tender)   Scrape CSV File. 
    [27/04/2022] (Still requires testing.)
- [x] (PPID)     Scrape CSV File. 
    [27/04/2022] (Still requires testing.)
- [ ] (Reciepts)  Scrape CSV File. 

Extra to add to above functions:
- [x] output Filename of file. [28/04/2022] ()
- [ ] Add check if no data found.
- [ ] Alter parameter to accept vURL from list.


###### sql.py (postgres)

Distinct Dates

    1) Open SQL connection.
    2) Read distinct dates the stored SQL.
    3) Return date list.

- [x] (Sales)    Get Distinct Dates in SQL. [24/04/2022] (Requires re-writing for generalisation) 
- [x] (Tender)   Get Distinct Dates in SQL. [24/04/2022] (Requires re-writing for generalisation)
- [x] (PPID)     Get Distinct Dates in SQL. [24/04/2022] (Requires re-writing for generalisation)
- [ ] (Reciepts) Get Distinct Dates in SQL.
- [ ] fuction:round date to hour. wrapper to be used when needed.


Import CSV to SQL

    1) Convert CSV into table.
    2) check table headers are valid.
    3) Open SQL connection.
    4) insert Table into SQL.

- [ ] (Sales)    Import CSV into SQL.
- [ ] (Tender)   Import CSV into SQL.
- [ ] (PPID)     Import CSV into SQL.
- [ ] (Reciepts) Import CSV into SQL.


Scrape CSV File into SQL.

    1) Open webbrowser
    2) Download report based on URL.
    2) check table headers are valid.
    3) Open SQL connection.
    4) insert Table into SQL.

- [x] (Sales)    Scrape CSV into SQL. [29/04/2022] ()
- [x] (Tender)   Scrape CSV into SQL. [29/04/2022] ()
- [x] (PPID)     Scrape CSV into SQL. [29/04/2022] ()
- [ ] (Reciepts) Scrape CSV into SQL.


###### SQL.CreateTable
Create sql structure if it doesn't already exist.

    1) Connect to database.
    2) Create table
    3) Close database.

- [ ] Sales
- [ ] Tender
- [ ] PPID
- [ ] Reciepts


###### SQL.CheckTable
Check the structure of the table is correct.

CheckTable()

    1) Connect to database.
    2) Query structure table column by coloumn.
    3) return list of issues.
    4) Close database.

- [ ] Sales
- [ ] Tender
- [ ] PPID
- [ ] Reciepts


---


## Future idea.
Unlikely addition but will review after completing everything else.

###### Dataframe output
Scrape csv and output dataframe.

###### Dataframe to SQL
Take dataframe and input into SQL. Biggest issue with this config is setting the data types. Everything will bee re-setting up.


