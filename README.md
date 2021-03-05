BOINC Monitor
===============
Attach to BOINC clients to extract statistics and/or control them; primary focus is capturing stats.

Using the original code, I moved things into a bit more of an Object Oriented code base with smaller/more focused components.

Acknowledgements
---------------
Source reference code(and project name) originates from: 

https://github.com/MestreLion/boinc-indicator

Included forked code to bring project up to Python 3 from:

https://github.com/drakej/boinc-indicator

Code from these projects is still largely visible in the original directory.


Requirements
---------------
Python3 

Reference requirements.txt for Python packages.  Suggest making a virtualenv and installing there.

``pip install -r requirements.txt``


Running
---------------
This will spin up a Flask webserver where you can start and stop threads for Boinc clients and InfluxDB clients which follow a producer/consumer model using a shared queue.

``python3 webui.py``


Configurations
---------------
Host configurations are contained in the file below along with a few variables for global usage.

api/constants.py