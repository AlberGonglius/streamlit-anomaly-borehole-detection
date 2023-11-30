from datetime import datetime, timedelta

def generate_range(start_date, end_date):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days)]

def get_datetime(day,month,year):
    return datetime(year,month,day,0,0,0)

def generate_range_hours(start_date, end_date):
    delta = end_date - start_date
    return [start_date + timedelta(hours=i) for i in range(int(delta.total_seconds()//3600))]