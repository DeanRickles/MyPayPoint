import datetime as datetime

# date valididation 
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, "%d/%m/%Y %H:%M:%S")
    except ValueError:
        raise ValueError("Incorrect data format, should be DD/MM/YYYY hh:mm:ss")
