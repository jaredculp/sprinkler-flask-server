sprinkler-flask-server
======================

What is this?
-------------

This Flask application serves as the front-end for our "smart" sprinkler system designed for our senior capstone design project at the University of Virginia in the Fall 2013 semester.

Installation
------------

Make sure you have python, pip, and virtualenv. Then run:

```bash
pip install -e venv -r ./requirements.txt
```

Activate the virtualenv with:

```bash
source venv/bin/activate
```

Run the server and database by invoking:

```bash
python server.py
```

Basic usage
-----------

Sprinklers can be manipulated in the following ways:

*   Add a new sprinkler to the system (give it a name)
*   Turn any existing sprinkler on/off
*   Turn all existing sprinklers on/off
*   Request status updates (on/off, flow and moisture readings)
*   Delete a sprinkler from the system
*   Delete all sprinklers from the system

This system is meant to be deployed on a central base station. During development we used a BeagleBone Black. The system is by no means "complete".

Communication is performed over UART to MSP430s running at each sprinkler head.

Authors
-------

[Alex Hutcheson](http://github.com/alexhutcheson), [Bryan Walsh](http://github.com/walshycakes), and [Jared Culp](http://github.com/jaredculp).

Feel free to fork or send a pull request!
