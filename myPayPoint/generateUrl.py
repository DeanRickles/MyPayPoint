'''
    Requirements:
        pip install urllib3
'''

# local modules
from . import urlParse
from . import validation as val # validation

# pip modules
import json

def TenderURL(vStartTimestamp,vEndTimeStamp,vPaymentMethod):
    '''
    Requirements:
        pip install urllib3
    
    Notes:
        Variables
            vStartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            vEndTimestamp   = End of timestamp wanted.                 
                Example format '20/01/2022 01:00:00'
            vPaymentMethod
                1 = Cash
                2 = Card
    '''
    
    # check date format
    val.validate(vStartTimestamp)
    val.validate(vEndTimeStamp)
    
    # based on type provide url breadcrumbs.
    if (vPaymentMethod == 1) or (vPaymentMethod == 2):
        if(vPaymentMethod == 1):
            vPaymentMethod = 'Cash'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"TenderGrouped","pageIndex":1,"pageSize":25,"groupByField":"tenderType","sortByField":"description","sortDirection":1,"filters":[],"filtersVisible":true,"dateRangeType":2,"reportsLength":0,"reportDateRangeEnum":2,"graphColumnSubindex":-1}},{"name":"Cash","data":{"reportTypeEnum":"TenderDetail","startDate":"10/3/2022 00:00:00","endDate":"10/3/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"1","sortByField":"dateTime","sortBySubindex":-1,"sortDirection":-1,"filters":[{"FilterName":"tenderType","FilterValues":[{"Id":"1","Value":"Cash","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"qty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
        else:
            vPaymentMethod = 'Card'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"TenderGrouped","pageIndex":1,"pageSize":25,"groupByField":"tenderType","sortByField":"description","sortDirection":1,"filters":[],"filtersVisible":true,"dateRangeType":2,"reportsLength":0,"reportDateRangeEnum":2}},{"name":"Card Payment","data":{"reportTypeEnum":"TenderDetail","startDate":"10/3/2022 00:00:00","endDate":"10/3/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"3","sortByField":"dateTime","sortBySubindex":-1,"sortDirection":-1,"filters":[{"FilterName":"tenderType","FilterValues":[{"Id":"3","Value":"Card Payment","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"qty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
    else:
        return print( '''vPaymentMethod input the corrisponding number:
                (1) = Cash
                (2) = Card''')
    
    vURLJsonQuery_Template[1]['data']['startDate'] = vStartTimestamp
    vURLJsonQuery_Template[1]['data']['endDate'] = vEndTimeStamp
       
    # template data
    vURLbody_Template  = 'https://my.paypoint.com/epos/epos-reporting?#/report?breadcrumbs='
    
    
    return vURLbody_Template + urlParse.urlEncode(json.dumps(vURLJsonQuery_Template))




def SalesURL(vStartTimestamp,vEndTimeStamp,vSaleType):
    '''
    Requirements:
        pip install urllib3
    
    Notes:
        Variables
            vStartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            vEndTimestamp   = End of timestamp wanted.                 
                Example format '20/01/2022 01:00:00'
            vSaleType
                1 = Standard Sales
                2 = Other Sales
    
    '''
    
    # check date format
    val.validate(vStartTimestamp)
    val.validate(vEndTimeStamp)
    
    
    # based on type provide url breadcrumbs.
    if (vSaleType == 1) or (vSaleType == 2):
        if(vSaleType == 1):
            vSaleType = 'Standard Sales'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"SalesGrouped","pageIndex":1,"pageSize":25,"groupByField":"isCommission","sortByField":"description","sortBySubindex":0,"sortDirection":1,"filters":[],"graphColumnName":"totalQty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":2,"reportsLength":1,"reportDateRangeEnum":2}},{"name":"Standard Sales","data":{"reportTypeEnum":"SalesDetail","startDate":"28/2/2022 00:00:00","endDate":"28/2/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"\\"$bsk.bskItems.product.productCategory.productCategoryId\\"","sortByField":"category","sortBySubindex":-1,"sortDirection":1,"filters":[{"FilterName":"isCommission","FilterValues":[{"Id":"false","Value":"Standard Sales","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"totalQty","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
        else:
            vSaleType = 'Other Sale'
            vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"SalesGrouped","pageIndex":1,"pageSize":25,"groupByField":"isCommission","sortByField":"description","sortBySubindex":0,"sortDirection":1,"filters":[],"graphColumnName":"totalQty","filtersVisible":true,"dateRangeType":2,"reportsLength":1,"reportDateRangeEnum":2}},{"name":"Other Sales","data":{"reportTypeEnum":"SalesDetail","startDate":"10/03/2022 00:00:00","endDate":"10/03/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByValue":"\\"$bsk.bskItems.product.productCategory.productCategoryId\\"","sortByField":"category","sortBySubindex":-1,"sortDirection":1,"filters":[{"FilterName":"isCommission","FilterValues":[{"Id":"true","Value":"Other Sales","IsSystemFilter":true}],"IsHiddenInSystemFilters":false}],"graphColumnName":"totalQty","filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')
    else:
        return print( '''vSaleType input the corrisponding number:
                (1) = Standard Sales
                (2) = Other Sales''')
    
    vURLJsonQuery_Template[1]['data']['startDate'] = vStartTimestamp
    vURLJsonQuery_Template[1]['data']['endDate'] = vEndTimeStamp
       
    # template data
    vURLbody_Template  = 'https://my.paypoint.com/epos/epos-reporting?#/report?breadcrumbs='
    
    return vURLbody_Template + urlParse.urlEncode(json.dumps(vURLJsonQuery_Template))


def PPIDURL(vStartTimestamp,vEndTimeStamp):
    '''
    Requirements:
        pip install urllib3
    
    Notes:
        Variables
            vStartTimestamp = begining of timestamp wanted.
                Example format '20/01/2022 00:00:00'
            vEndTimestamp   = End of timestamp wanted.                 
                Example format '20/01/2022 01:00:00'
    '''
    
    # check date format
    val.validate(vStartTimestamp)
    val.validate(vEndTimeStamp)
    
    # based on type provide url breadcrumbs.
    vURLJsonQuery_Template = json.loads('[{"name":"All","data":{"reportTypeEnum":"PayPointDetail","startDate":"10/4/2022 00:00:00","endDate":"10/4/2022 23:59:59","pageIndex":1,"pageSize":25,"groupByField":"noGrouping","sortByField":"time","sortBySubindex":0,"sortDirection":1,"filters":[],"graphColumnName":"amount","graphColumnSubindex":-1,"filtersVisible":true,"dateRangeType":1,"reportsLength":1}}]')

    vURLJsonQuery_Template[0]['data']['startDate'] = vStartTimestamp
    vURLJsonQuery_Template[0]['data']['endDate'] = vEndTimeStamp
       
    # template data
    vURLbody_Template  = 'https://my.paypoint.com/epos/epos-reporting?#/report?breadcrumbs='  
    
    return vURLbody_Template + urlParse.urlEncode(json.dumps(vURLJsonQuery_Template))