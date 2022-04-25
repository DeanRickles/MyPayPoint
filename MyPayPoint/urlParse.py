import urllib.parse 

def urlDecode(vURLQuery):
    return (urllib.parse.unquote_to_bytes(urllib.parse.unquote_plus(vURLQuery))).decode('utf-8')

def urlEncode(vURLQuery):
    return urllib.parse.quote_plus(urllib.parse.quote_from_bytes(vURLQuery.encode('utf-8')))