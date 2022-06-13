# MyPayPoint

#### Introduction
Python script to scrape https://my.paypoint.com reports of the webiste and into Postgress.

Script is broken into modules and can be altered to suit the user.

---

#### To Do:
This section is purely to help me keep on track and note what needs to be done.

Starting with Sales and then add each catagory type after.


##### Bug fixes:
- [x] Standardise datetime header. datetime = StartDate && enddatetime = Enddate
    - [x] checked datePeriod.py
    - [x] checked downloadReport.py
    - [x] checked generateURL.py
    - [x] checked Report_to_sql.py
    - [x] checked sql.py
- [x] Move SQL queries to own module.
- [x] Pacman requirement file.
- [x] PIP requirement file.
- [ ] Scope out all varaibles and remove any unrequired.
- [x] Replace time.sleep() with selenium wait.
- [ ] Review variable notes in each function.
- [ ] Issue with barcodes not always importing
- [x] move unmanaged resources into with function.

##### datePeriod.py

- [x] compare_date_list
- [x] datespan
- [x] filter_workfay
- [x] hour_end
- [x] distinct_datetime

##### urlParse.py
- [x] (URL parse) Decode.
- [x] (URL parse) Encode.


##### generateUrl.py

*Type*URL(datetime,enddatetime,type)

    1) using  selected inputs manulate a breadcrumb URL for downloadReport.

- [x] (Sales)   generateURL
- [x] (Tender)  generateURL
- [x] (PPID)    generateURL
- [x] (Receipts) generateURL


##### downloadReport.py

Scrape CSV File.

    1) Open webbrowser
    2) Download report based on URL.
    3) Return list of file paths.

- [x] (Sales)    Scrape CSV File.
- [x] (Tender)   Scrape CSV File.
- [x] (PPID)     Scrape CSV File.
- [x] (Receipts)  Scrape CSV File.

Extra to add to above functions:
- [x] output Filename of file.
- [ ] Add check if no data found.
- [ ] Update sleep into selenium wait.



##### sql.py (postgres)

Distinct Dates

    1) Open SQL connection.
    2) Read distinct dates the stored SQL.
    3) Return date list.

- [x] (Sales)    Get Distinct Dates in SQL.
- [x] (Tender)   Get Distinct Dates in SQL.
- [x] (PPID)     Get Distinct Dates in SQL.
- [x] (Receipts) Get Distinct Dates in SQL.


Scrape CSV File into SQL.

    1) Open webbrowser
    2) Download report based on URL.
    2) check table headers are valid.
    3) Open SQL connection.
    4) insert Table into SQL.

- [x] (Sales)    Scrape CSV into SQL.
- [x] (Tender)   Scrape CSV into SQL.
- [x] (PPID)     Scrape CSV into SQL.
- [x] (Receipts) Scrape CSV into SQL.


Import CSV to SQL

    1) Convert CSV into table.
    2) check table headers are valid.
    3) Open SQL connection.
    4) insert Table into SQL.

- [ ] (Sales)    Import CSV into SQL.
- [ ] (Tender)   Import CSV into SQL.
- [ ] (PPID)     Import CSV into SQL.
- [ ] (Receipts) Import CSV into SQL.


##### SQL.CreateTable
Create sql structure if it doesn't already exist.

    1) Connect to database.
    2) Create table
    3) Close database.

- [ ] Sales
- [ ] Tender
- [ ] PPID
- [x] Receipts


##### SQL.CheckTable
Check the structure of the table is correct.

CheckTable()

    1) Connect to database.
    2) Query structure table column by coloumn.
    3) return list of issues.
    4) Close database.

- [ ] Sales
- [ ] Tender
- [ ] PPID
- [ ] Receipts
