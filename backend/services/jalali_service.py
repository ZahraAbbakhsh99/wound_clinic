import jdatetime
from datetime import datetime


def jalali_start_of_week():
    """
    Returns the start of the current Jalali week (Saturday) 
    as a Gregorian datetime at 00:00 local time
    """
    today_j = jdatetime.date.today()         # current Jalali date
    weekday = today_j.weekday()              # Saturday=0 ... Friday=6

    # We want Saturday (weekday 0)
    days_to_saturday = weekday               # days since Saturday

    start_jalali = today_j - jdatetime.timedelta(days=days_to_saturday)

    # Convert to Gregorian at midnight
    start_gregorian = jdatetime.datetime(
        start_jalali.year,
        start_jalali.month,
        start_jalali.day,
        0, 0, 0
    ).togregorian()

    return start_gregorian


def jalali_start_of_month():
    """
    Returns the start of the current Jalali month
    converted to a Gregorian datetime.
    """
    today = jdatetime.date.today()
    start_jalali = jdatetime.date(today.year, today.month, 1)

    g_date = start_jalali.togregorian()

    return datetime.combine(g_date, datetime.min.time())


def jalali_today_start():
    """
    Returns today's date start (00:00) in Gregorian datetime.
    """
    today = jdatetime.date.today()

    g_date = today.togregorian()

    return datetime.combine(g_date, datetime.min.time())
