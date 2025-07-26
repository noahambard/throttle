"""
test.py

Tests functionality for throttle.py

Written by Noah Emmanuel Ambard
"""

from collections.abc import Callable
from functools import update_wrapper
from throttle import ThrottledTask, DebouncedTask
from sys import exit
from time import sleep


BLUE   = "\033[94m"
GREEN  = "\033[92m"
RED    = "\033[91m"
RESET  = "\033[0m"
YELLOW = "\033[93m"

tests: list[Callable[..., None]] = []


"""
Catch any Assertion Errors in func and register func as a new test
"""
def testcase(test_name: str) -> Callable[[Callable], Callable[..., None]]:
    def decorator(func: Callable):
        global tests

        def wrapper(*args, **kwargs) -> None:
            try:
                func(*args, **kwargs)
                print(GREEN + "> " + BLUE + f"{test_name} " + GREEN +
                      "passed\n" + RESET)
            except AssertionError as err:
                print(YELLOW + f"{test_name} " + RED +
                      f"failed:\n> {err}\n\n" + RESET)
                exit(1)

        update_wrapper(wrapper, func)
        tests += [wrapper]

        return wrapper
        
    return decorator


"""
Tests a simple throttled task
"""
@testcase("Test 1 (Throttle)")
def test1() -> None:
    numbers = ["one", "two"]

    def add_number(numbers: list[str]):
         numbers += ["three"]

    task = ThrottledTask(0.5, add_number, numbers)

    assert task.is_ready(), "is_ready() returned False before ever being run"

    task.run_if_ready()
    assert numbers == ["one", "two", "three"], "Task didn't run correctly"

    assert not task.is_ready(), "is_ready() returned True just after being run"

    sleep(0.5)
    assert task.is_ready(), "is_ready() returned False after interval elapsed"


"""
Tests a simple debounced task
"""
@testcase("Test 2 (Debounce)")
def test2() -> None:
    numbers = ["three", "two"]

    def add_number(numbers: list[str]):
        numbers += ["one"]
    
    task = DebouncedTask(0.3, add_number, numbers)

    assert task.is_ready(), "is_ready() returned False before ever being run"

    task.run_if_ready()
    assert numbers == ["three", "two", "one"], "Task didn't run correctly"

    assert not task.is_ready(), "is_ready() returned True just after being run"

    sleep(0.15)
    assert not task.is_ready(), "is_ready() returned True before interval elapsed"
    sleep(0.15)
    assert not task.is_ready(), "is_ready() returned True before interval elapsed"
    sleep(0.3)
    assert task.is_ready(), "is_ready() returned False after interval elapsed"


if __name__ == "__main__":
    for test in tests:
        test()
    print()
