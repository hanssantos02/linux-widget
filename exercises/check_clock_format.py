from datetime import datetime
from exercises.clock_format import format_time

date_1 = datetime(2026, 10, 18, 14, 7, 9)
date_2 = datetime(2026, 10, 18, 14, 7, 9)
date_3 = datetime(2026, 10, 18, 0, 0, 5)
date_4 = datetime(2026, 10, 18, 12, 0, 0)

assert format_time(date_1) == "14:07:09"
assert format_time(date_2, False) == "02:07:09 PM"
assert format_time(date_3, False) == "12:00:05 AM"
assert format_time(date_4, False) == "12:00:00 PM"

print("All formatter checks passed")
