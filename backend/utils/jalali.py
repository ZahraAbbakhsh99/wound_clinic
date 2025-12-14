import jdatetime
from datetime import datetime

def jalali_to_gregorian(jalali_str: str) -> datetime:
    """
    Convert Jalali date string 'YYYY-MM-DD HH:MM' to Gregorian datetime.
    """
    date_part, time_part = jalali_str.split()
    year, month, day = map(int, date_part.split('-'))
    hour, minute = map(int, time_part.split(':'))
    return jdatetime.datetime(year, month, day, hour, minute).togregorian()

def gregorian_to_jalali(gregorian_dt: datetime) -> str:
    """
    Convert Gregorian datetime to Jalali date string 'YYYY-MM-DD HH:MM'.
    """
    jalali_dt = jdatetime.datetime.fromgregorian(datetime=gregorian_dt)
    return jalali_dt.strftime("%Y-%m-%d %H:%M")


def to_jalali(dt):
    """Convert a Gregorian datetime to Jalali string YYYY/MM/DD HH:MM"""
    if dt is None:
        return ""
    jalali_dt = jdatetime.datetime.fromgregorian(datetime=dt)
    return jalali_dt.strftime("%Y/%m/%d %H:%M")


def to_jalali_parts(dt: datetime):
    """Return (date, time) separately"""
    if dt is None:
        return "", ""

    jalali_dt = jdatetime.datetime.fromgregorian(datetime=dt)

    date_str = jalali_dt.strftime("%Y/%m/%d")
    time_str = jalali_dt.strftime("%H:%M")

    return date_str, time_str
