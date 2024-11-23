from datetime import datetime, timezone

def generate_utc0_millisecond_timestamp():
    """TODO: Doc"""
    return int(datetime.now(tz=timezone.utc).timestamp() * 1e3)