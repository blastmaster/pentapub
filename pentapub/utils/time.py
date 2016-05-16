from datetime import date, timedelta, time


def get_fourth_tuesday(month):
    ''' calculates the fourth tuesday of the given month
        returns a timedelta from the start of the month.

        Assumes that the day of the month is 1. '''

    if month.weekday() < 1:
        # Month starts before tuesday
        return timedelta(weeks=3, days=1)
    elif month.weekday() == 1:
        # Month starts at tuesday
        return timedelta(weeks=3)
    else:
        # Month starts after tuesday
        day_offset = 7 - month.weekday() + 1
        return timedelta(weeks=3, days=day_offset)


def get_rec_date(year=None, month=None):
    ''' Returns the date of a pentaradio recording as datetime.date object.
        It is possible to pass a year and a month of a recording to get the date
        of a specific pentaradio. year and month must be integers. '''

    today = date.today()

    if not year:
        year = today.year

    if not month or month not in range(1,12):
        month = today.month

    month_obj = date(year=year,
                 month=month,
                 day=1)
    delta = get_fourth_tuesday(month_obj)
    return month_obj + delta


def seconds_to_time(seconds):
    ''' get seconds return a HMS time object '''

    h = int(seconds / 3600)
    m = int(seconds / 60) - h * 60
    s = seconds % 60

    return time(hour=h, minute=m, second=s)
