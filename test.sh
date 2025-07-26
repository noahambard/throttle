# Runs tests for throttle.py
# 
# Written by Noah Emmanuel Ambard

printf '\033[94mmypy:\033[0m\n'
mypy throttle.py test.py

printf '\n\n\033[94mtest.py:\033[0m\n'
python3 test.py
