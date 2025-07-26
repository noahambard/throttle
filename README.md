# throttle.py

Contains utility classes for tasks which can be run at some interval.

Written by Noah Emmanuel Ambard

## Example program

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
