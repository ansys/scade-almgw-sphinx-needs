Cruise speed management
=======================

.. hlr:: Manage
   :id: CC_HLR_CSM_01
   :collapse: true

   The cruise speed shall be managed only when the cruise control is enabled, meaning ``ON``, ``STDBY``, or ``INT`` states.

.. hlr:: Set
   :id: CC_HLR_CSM_02
   :collapse: true

   The cruise speed shall be set to the current speed when the set button is pressed.

.. hlr:: Accelerate
   :id: CC_HLR_CSM_03
   :collapse: true

   The cruise speed shall be increased of ``SPEED_INC`` when the quick accel button is pressed, with respect to ``SPEED_MAX``.

.. hlr:: Decelerate
   :id: CC_HLR_CSM_04
   :collapse: true

   The cruise speed shall be decreased of ``SPEED_INC`` when the quick decel button is pressed, with respect to ``SPEED_MIN``.

.. hlr:: Regulation
   :id: CC_HLR_CSM_05
   :collapse: true

   The cruise speed shall be maintained between ``SPEED_MIN`` and ``SPEED_MAX``.

.. hlr:: Stable
   :id: CC_HLR_CSM_06
   :collapse: true

   The cruise speed shall remain identical when none of the buttons set, quick accel and quick decel are pressed.
