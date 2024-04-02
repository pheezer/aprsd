import datetime
import tracemalloc

from oslo_config import cfg

import aprsd
from aprsd import utils


CONF = cfg.CONF


class APRSDStats:
    """The AppStats class is used to collect stats from the application."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Have to override the new method to make this a singleton

        instead of using @singletone decorator so the unit tests work.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.start_time = datetime.datetime.now()

    def uptime(self):
        return datetime.datetime.now() - self.start_time

    def stats(self, serializable=False) -> dict:
        current, peak = tracemalloc.get_traced_memory()
        uptime = self.uptime()
        if serializable:
            uptime = str(uptime)
        stats = {
            "version": aprsd.__version__,
            "uptime": uptime,
            "callsign": CONF.callsign,
            "memory_current": int(current),
            "memory_current_str": utils.human_size(current),
            "memory_peak": int(peak),
            "memory_peak_str": utils.human_size(peak),
        }
        return stats
