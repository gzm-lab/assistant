from datetime import datetime,timezone,timedelta 

test = int("1734289078")


cet_timezone = timezone(timedelta(hours=1))

print(datetime.fromtimestamp(test, tz=cet_timezone))