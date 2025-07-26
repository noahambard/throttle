"""
throttle.py

Contains utility classes for tasks which can be run at some interval.

Written by Noah Emmanuel Ambard
"""

from collections.abc import Callable
from time import time
from typing import Any


class _TimedTask:
    """
    An abstract class which represents a task which can be run at some interval
    """

    def __init__(self, interval_s: float, task: Callable, *args, **kwargs):
        """
        Creates a new object which can do some task at some interval.

        interval_s : float
            The minimum interval between running the task in seconds. May have
            fractions of a second depending on the system
        task: Callable
            The task that can be run
        
        Any additional positional or keyword arguments will get passed to the
        task when run
        """

        self._interval_s = interval_s
        self._last_activate_s: float = time() - self._interval_s
        self._task = task
        self._args = args
        self._kwargs = kwargs


    def get_args(self) -> tuple:
        """
        Returns the positional arguments to be passed to the task
        """

        return self._args


    def get_kwargs(self) -> dict[str, Any]:
        """
        Returns the keyword arguments to be passed to the task
        """

        return self._kwargs


    def get_interval_s(self) -> float:
        """
        Returns the minimum interval between running the task in seconds. May have
        fractions of a second depending on the system
        """

        return self._interval_s


    def get_last_activate_s(self) -> float:
        """
        Returns the last time the task was run in seconds. May have fractions
        of a second depending on the system.
        After this object is first created, this method returns the time of
        creation minus `get_interval_s()`
        """

        return self._last_activate_s


    def get_task(self) -> Callable:
        """
        Returns the task that can be run
        """

        return self._task


    def is_ready(self) -> bool:
        """
        Returns whether this task is ready to be run.
        IMPORTANT: Must be implemented by a subclass
        """

        return False


    def run(self) -> None:
        """
        Runs the task with positional and keyword arguments, and updates the time
        last activated
        """

        self._task(*self._args, **self._kwargs)
        self._last_activate_s = time()


    def run_if_ready(self) -> None:
        """
        Runs the task if `is_ready()` returns True
        """

        if self.is_ready():
            self.run()


class DebouncedTask(_TimedTask):
    """
    Represents a task which can only be run after an interval amount of seconds
    of NOT being attempted to run
    """

    def is_ready(self) -> bool:
        """
        Returns whether this task is ready to run. If it isn't, the timer will
        reset, thus debouncing this task
        """

        if time() - self._last_activate_s < self._interval_s:
            self._last_activate_s = time()
            return False
        return True


class ThrottledTask(_TimedTask):
    """
    Represents a task which can only be run after an interval amount of seconds
    since last being ran
    """
    
    def is_ready(self) -> bool:
        """
        Returns whether enough time has elapsed since the last time this task
        has run
        """
        
        return time() - self._last_activate_s >= self._interval_s

