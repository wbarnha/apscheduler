from datetime import timedelta, datetime
from math import ceil

from tzlocal import get_localzone

from apscheduler.triggers.base import BaseTrigger
from apscheduler.util import convert_to_datetime, timedelta_seconds, datetime_repr, astimezone


class IntervalTrigger(BaseTrigger):
    def __init__(self, weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, timezone=None):
        """
        Triggers on specified intervals, starting on ``start_date`` if specified, ``datetime.now()`` + interval
        otherwise.

        :param int weeks: number of weeks to wait
        :param int days: number of days to wait
        :param int hours: number of hours to wait
        :param int minutes: number of minutes to wait
        :param int seconds: number of seconds to wait
        :param datetime|str start_date: when to first execute the job and start the counter (default is after the given
                                        interval)
        :param datetime.tzinfo|str timezone: time zone for ``start_date``
        """

        self.interval = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
        self.interval_length = timedelta_seconds(self.interval)
        if self.interval_length == 0:
            self.interval = timedelta(seconds=1)
            self.interval_length = 1

        self.timezone = astimezone(timezone) or get_localzone()
        start_date = start_date or datetime.now(self.timezone) + self.interval
        self.start_date = convert_to_datetime(start_date, self.timezone, 'start_date')

    def get_next_fire_time(self, start_date):
        if start_date < self.start_date:
            return self.start_date

        timediff_seconds = timedelta_seconds(start_date - self.start_date)
        next_interval_num = int(ceil(timediff_seconds / self.interval_length))
        next_date = self.start_date + self.interval * next_interval_num
        return self.timezone.normalize(next_date)

    def __str__(self):
        return 'interval[%s]' % str(self.interval)

    def __repr__(self):
        return "<%s (interval=%r, start_date='%s')>" % (self.__class__.__name__, self.interval,
                                                        datetime_repr(self.start_date))
