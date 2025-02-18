Architecture notes
==================

The cruise control interface has been introduced in the :doc:`Interface <requirements/interface>` section.

When the cruise control is enabled, a first part computes the target cruise speed
and the other one ensures the regulation:

.. image:: /_static/architecture.png
  :alt: Cruise control architecture

The ``CruiseRegulation`` function is part of ``RegulationMngt``
and implements the algorithm described in :need:`CC_HLR_CDC_03 <CC_HLR_CDC_03>`.

.. image:: /_static/regulation.png
  :alt: Cruise control regulation
