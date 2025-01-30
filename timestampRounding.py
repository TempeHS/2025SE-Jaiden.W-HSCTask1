from datetime import datetime, timedelta, timezone

def round_to_nearest_15_minutes(dt):
    # Round to the nearest 15 minutes
    discard = timedelta(minutes=dt.minute % 15, seconds=dt.second, microseconds=dt.microsecond)
    dt -= discard
    if discard >= timedelta(minutes=7.5):
        dt += timedelta(minutes=15)
    return dt.replace(second=0, microsecond=0)

def get_rounded_timestamp():
    now = datetime.now(timezone.utc)
    rounded = round_to_nearest_15_minutes(now)
    return rounded.strftime('%Y-%m-%d %H:%M:%S')  # Formatted as 'YYYY-MM-DD HH:MM:SS'