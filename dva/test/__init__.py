import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module == 'testcase.py' or module[-3:] != '.py':
        continue
    # Dynamically import all testcases in directory.
    __import__(module[:-3], locals(), globals())
del module
del os

