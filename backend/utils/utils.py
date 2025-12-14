
def calculate_progress(this_week_count: int, last_week_count: int):
    if last_week_count == 0:
        if this_week_count == 0:
            percent_change = 0
        else:
            percent_change = 100
    else:
        percent_change = ((this_week_count - last_week_count) / last_week_count) * 100
    percent_change = round(percent_change)
    
    formatted = f"{percent_change:+d}%"
    return formatted
