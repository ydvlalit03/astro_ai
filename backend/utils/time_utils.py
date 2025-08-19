from datetime import datetime

def iso(dt):
    return dt.isoformat() if dt else None