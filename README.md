# MyPayPoint

#### Introduction
Python script to scrape https://my.paypoint.com reports of the webiste and into Postgress.

Script is broken into modules and can be altered to suit the user.

---

#### To Do:
This section is purely to help me keep on track and note what needs to be done.

Starting with Sales and then add each catagory type after.


###### General:
- [ ] Scope out all varaibles and remove any unrequired.
- [ ] Move main varaibles into .env
- [ ] Pacman requirement file.
- [ ] PIP requirement file.
- [ ] Standardise datetime header. Datetime = StartDate && endDateTime = Enddate
- [ ] Move SQL qeruies own module.
- [ ] Review variable notes in each function.

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
- [ ] (Recepts) generateURL
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
- [ ] (Recepts)  Scrape CSV File. 


###### sql.py (postgres)

Distinct Dates

    1) Open SQL connection.
    2) Read distinct dates the stored SQL.
    3) Return date list.

- [x] (Sales)    Get Distinct Dates in SQL. [24/04/2022] (Requires re-writing for generalisation) 
- [x] (Tender)   Get Distinct Dates in SQL. [24/04/2022] (Requires re-writing for generalisation)
- [x] (PPID)     Get Distinct Dates in SQL. [24/04/2022] (Requires re-writing for generalisation)
- [ ] (Reciepts) Get Distinct Dates in SQL.

Import CSV to SQL

    1) Convert CSV into table.
    2) Open SQL connection.
    3) insert Table into SQL.

- [ ] (Sales)   Import CSV into SQL.
- [ ] (Tender)  Import CSV into SQL.
- [ ] (PPID)    Import CSV into SQL.
- [ ] (Recepts) Import CSV into SQL.