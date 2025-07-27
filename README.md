# throttle.py

Contains utility classes for tasks which can be run at some interval.

Written by Noah Emmanuel Ambard

## Example 1

Debounces a button to correct for any input noise and continuously blinks an LED
every 1.75 seconds.

```py
from throttle import DebouncedTask, ThrottledTask
from sys import exit


button = ...
led = ...

# LED can only be toggled every 1.75 seconds
blinkTask = ThrottledTask(1.75, led.toggle)
# Can only pause LED if button has had 0.1 seconds of break time.
# Extra arguments for the task can be passed in after it
pauseTask = DebouncedTask(0.1, led.pause, led.LOW, 60)


while True:
    if button.is_pressed():
        # Debounce button input
        pauseTask.run_if_ready()
    
    # Blink LED every 1.75 seconds
    blinkTask.run_if_ready()
```

## Example 2

Manages many unrelated throttled tasks at once.

```py
from throttle import ThrottledTask


...

# Define all throttled tasks here. Tasks can be added or removed afterwards
tasks = [ThrottledTask(1, deviceOnLED.toggle),
         ThrottledTask(5, buzzer.beep(length=1)), ...]


while True:
    # Handle throttled tasks
    for task in tasks:
        task.run_if_ready()
```
