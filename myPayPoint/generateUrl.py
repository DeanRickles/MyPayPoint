'''
    Requirements:
        pip install urllib3
'''

# local modules
from . import urlParse # Pasrisng json data from url.
from . import validation as val # validation

# pip modules
import json

def TenderURL(StartTimestamp, EndTimeStamp, PaymentMethod):
    '''
    Requirements:
        pip install urllib3
    
    Notes:
        Variables
            StartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            EndTimeStamp   = End of timestamp wanted.
                Example format '20/01/2022 01:00:00'
            PaymentMethod
                1 = Cash
                2 = Card
    '''
    
    # check date format
    val.validate(StartTimestamp)
    val.validate(EndTimeStamp)
    
    # based on type provide url breadcrumbs.
    if (PaymentMethod == 1) or (PaymentMethod == 2):
        if(PaymentMethod == 1):
            PaymentMethod = 'Cash'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"TenderGrouped","pageIndex":1,"pageSize":25,"groupByField":"tenderType","sortByField":"description","sortDirection":1,"filters":[],"filtersVisible":true,"dateRangeType":2,"reportsLength":0,"reportDateRangeEnum":2,"graphColumnSubindex":-1}},{"name":"Cash","data":{"reportTypeEnum":"TenderDetail","startDate":"10/3/2022 00:00:00","endDate":"10/3/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"1","sortByField":"dateTime","sortBySubindex":-1,"sortDirection":-1,"filters":[{"FilterName":"tenderType","FilterValues":[{"Id":"1","Value":"Cash","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"qty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
        else:
            PaymentMethod = 'Card'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"TenderGrouped","pageIndex":1,"pageSize":25,"groupByField":"tenderType","sortByField":"description","sortDirection":1,"filters":[],"filtersVisible":true,"dateRangeType":2,"reportsLength":0,"reportDateRangeEnum":2}},{"name":"Card Payment","data":{"reportTypeEnum":"TenderDetail","startDate":"10/3/2022 00:00:00","endDate":"10/3/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"3","sortByField":"dateTime","sortBySubindex":-1,"sortDirection":-1,"filters":[{"FilterName":"tenderType","FilterValues":[{"Id":"3","Value":"Card Payment","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"qty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
    else:
        return print( '''PaymentMethod input the corrisponding number:
                (1) = Cash
                (2) = Card''')
    
    vURLJsonQuery_Template[1]['data']['startDate'] = StartTimestamp
    vURLJsonQuery_Template[1]['data']['endDate'] = EndTimeStamp
       
    # template data
    vURLbody_Template  = 'https://my.paypoint.com/epos/epos-reporting?#/report?breadcrumbs='
    
    
    return vURLbody_Template + urlParse.urlEncode(json.dumps(vURLJsonQuery_Template))




def SalesURL(StartTimestamp, EndTimeStamp, SaleType):
    '''
    Requirements:
        pip install urllib3
    
    Notes:
        Variables
            StartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            EndTimeStamp   = End of timestamp wanted.
                Example format '20/01/2022 01:00:00'
            SaleType
                1 = Standard Sales
                2 = Other Sales
    '''
    
    # check date format
    val.validate(StartTimestamp)
    val.validate(EndTimeStamp)
    
    # based on type provide url breadcrumbs.
    if (SaleType == 1) or (SaleType == 2):
        if(SaleType == 1):
            SaleType = 'Standard Sales'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"SalesGrouped","pageIndex":1,"pageSize":25,"groupByField":"isCommission","sortByField":"description","sortBySubindex":0,"sortDirection":1,"filters":[],"graphColumnName":"totalQty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":2,"reportsLength":1,"reportDateRangeEnum":2}},{"name":"Standard Sales","data":{"reportTypeEnum":"SalesDetail","startDate":"28/2/2022 00:00:00","endDate":"28/2/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"\\"$bsk.bskItems.product.productCategory.productCategoryId\\"","sortByField":"category","sortBySubindex":-1,"sortDirection":1,"filters":[{"FilterName":"isCommission","FilterValues":[{"Id":"false","Value":"Standard Sales","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"totalQty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
        else:
            SaleType = 'Other Sale'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"SalesGrouped","pageIndex":1,"pageSize":25,"groupByField":"isCommission","sortByField":"description","sortBySubindex":0,"sortDirection":1,"filters":[],"graphColumnName":"totalQty","filtersVisible":true,"dateRangeType":2,"reportsLength":1,"reportDateRangeEnum":2}},{"name":"Other Sales","data":{"reportTypeEnum":"SalesDetail","startDate":"10/03/2022 00:00:00","endDate":"10/03/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"\\"$bsk.bskItems.product.productCategory.productCategoryId\\"","sortByField":"category","sortBySubindex":-1,"sortDirection":1,"filters":[{"FilterName":"isCommission","FilterValues":[{"Id":"true","Value":"Other Sales","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"totalQty","filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
    else:
        return print( '''SaleType input the corrisponding number:
                (1) = Standard Sales
                (2) = Other Sales''')
    
    vURLJsonQuery_Template[1]['data']['startDate'] = StartTimestamp
    vURLJsonQuery_Template[1]['data']['endDate'] = EndTimeStamp
       
    # template data
    vURLbody_Template  = 'https://my.paypoint.com/epos/epos-reporting?#/report?breadcrumbs='
    
    return vURLbody_Template + urlParse.urlEncode(json.dumps(vURLJsonQuery_Template))


def PPIDURL(StartTimestamp, EndTimeStamp):
    '''
    Requirements:
        pip install urllib3
    
    Notes:
        Variables
            StartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            EndTimeStamp   = End of timestamp wanted.
                Example format '20/01/2022 01:00:00'
    '''
    
    # check date format
    val.validate(StartTimestamp)
    val.validate(EndTimeStamp)
    
    # based on type provide url breadcrumbs.
    vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"PayPointDetail","startDate":"10/4/2022 00:00:00","endDate":"10/4/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByField":"noGrouping","sortByField":"time","sortBySubindex":0,"sortDirection":1,"filters":[],"graphColumnName":"amount","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')

    vURLJsonQuery_Template[0]['data']['startDate'] = StartTimestamp
    vURLJsonQuery_Template[0]['data']['endDate'] = EndTimeStamp
    
    # template data
    vURLbody_Template  = 'https://my.paypoint.com/epos/epos-reporting?#/report?breadcrumbs='
    
    return vURLbody_Template + urlParse.urlEncode(json.dumps(vURLJsonQuery_Template))


def receiptURL(StartTimestamp, EndTimeStamp):
    '''
    Requirements:
        pip install urllib3

    Notes:
        Variables
            StartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            EndTimeStamp   = End of timestamp wanted.
                Example format '20/01/2022 01:00:00'
    '''
    
    # check date format
    val.validate(StartTimestamp)
    val.validate(EndTimeStamp)
    
    # template url data
    URL = "https://my.paypoint.com/epos/epos-reporting#/receipt-viewer?filters=%255B%255D&sortColumn=Date%20DESC&graphColumn=&groupBy=1&userReportId=0&breadcrumb=%5B%7B%22Id%22:%22-1%22,%22Type%22:0%7D%5D&startDateTime=2022-05-10-00-00-00&endDateTime=2022-05-10-23-00-59"
    URLstartDate = "2022-05-10-00-00-00"
    URLendDate   = "2022-05-10-23-00-59"
    
    # transform inputed datetime to format wanted and replace in url for return. Only issue is milliseconds but who would filter using milliseconds?
    newStartDate = datetime.strptime(StartTimestamp, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d-%H-%M-%S-00')
    newEndDate   = datetime.strptime(EndTimeStamp, "%d/%m/%Y %H:%M:%S").strftime('%Y-%m-%d-%H-%M-%S-59')
    
    return URL.replace(URLstartDate,newStartDate).replace(URLendDate,newEndDate)