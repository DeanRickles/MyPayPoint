from datetime import datetime
from datetime import timedelta
from myPayPoint import datePeriod as dp, downloadReport as dr, generateUrl, sql

# Varaibles used.
vSite = '' # siteid_email
vUser = ''  # username
vPass = '' # password
vServerIP   = '' # Postgress Server
vServerPort = '5432' # Pogress port
vServerDB   = '' # Database name
vServerUser = '' # Username
vServerPass = '' 

# Clear and create vURL list.
vURL = []

# generate range of dates by hour.
vdateSpan = dp.filter_workday(dp.datespan(
                                datetime.today() - timedelta(days=1),
                                datetime.today() - timedelta(hours=1)
                            ))

# Get Sales SQL dates
vStartDate = dp.compare_datetime_list(vdateSpan,
                                      dp.distinct_datetime(dp.hour_rounder(sql.GetDateTime(vServerIP, vServerPort, vServerDB, 'REPORTDATA', vServerUser, vServerPass))))

# sorts data. Not required but helpfull.
vStartDate.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y %H:%M:%S"), reverse=True)

# Generate enddate
vEndDate = dp.hour_end(vStartDate)

# used to create the URL with both reports.
for x in range(len(vStartDate)):
    vURL.append(generateUrl.SalesURL(vStartDate[x],vEndDate[x],1))
    vURL.append(generateUrl.SalesURL(vStartDate[x],vEndDate[x],2))

# clear variable
del vdateSpan
del vStartDate
del vEndDate

# only run for 24 reports.
sql.SalesReport_to_SQL(vURL[:24],
                       vSite=vSite,
                       vUser=vUser,
                       vPass=vPass,
                       vServerIP=vServerIP,
                       vServerPort=vServerPort,
                       vServerDB=vServerDB,
                       vServerTbl='REPORTDATA',
                       vServerUser=vServerUser,
                       vServerPass=vServerPass)