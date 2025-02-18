Interface
=========

The Cruise Control (CC) connects to the system using the following inputs:

* ``on`` (``bool``): Enable the CC
* ``off`` (bool``): Disable the CC
* ``resume_`` (bool``): Resume the CC after a braking
* ``set`` (``bool``): Set the current speed as the new cruise speed
* ``quickDecel`` (``bool``): Decrease the cruise speed
* ``quickAccel`` (``bool``): Increase the cruise speed
* ``accel`` (``float32``, percentage): Accelerator pedal sensor
* ``brake`` (``float32``, percentage): Brake pedal sensor
* ``speed`` (``float32``, km/h): Car speed sensor

The CC provides the following outputs:

* ``cruiseSpeed`` (``float32``, km/h): Cruise speed value
* ``throttleCmd`` (``float32``, percentage): Throttle command
* ``cruiseState`` (``OFF``, ``ON``, ``STDBY``, or ``INT``): CC’s state

The following diagram summarizes the CC interface:

.. image:: /_static/interface.png
  :alt: Cruise control interface
