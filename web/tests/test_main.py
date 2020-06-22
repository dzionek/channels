from datetime import datetime
from app.main.utils import pretty_time

class TestUtils:
    def test_pretty_time(self) -> None:
        date1 = datetime(year=2000, month=1, day=7, hour=1, minute=30)
        date2 = datetime(year=2077, month=10, day=29, hour=0, minute=0)
        date3 = datetime(year=2040, month=7, day=31, hour=23, minute=59)
        assert pretty_time(date1) == '2000-01-07 01:30'
        assert pretty_time(date2) == '2077-10-29 00:00'
        assert pretty_time(date3) == '2040-07-31 23:59'
