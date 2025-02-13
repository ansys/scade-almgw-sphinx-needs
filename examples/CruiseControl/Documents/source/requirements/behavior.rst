Cruise control behavior
=======================

.. hlr:: Initial state
   :id: CC_HLR_CCB_01

   When the driver starts the car, the CC shall be off.

   The output ``cruiseState`` should be set to ``OFF``.

.. hlr:: Activation
   :id: CC_HLR_CCB_02
   :collapse: true

   The CC shall be on when the driver pushes the On button.

   The output ``cruiseState`` shall be different from ``OFF`` e.g., one of ``ON``, ``STDBY``, or ``INT``.

.. hlr:: Off
   :id: CC_HLR_CCB_03
   :collapse: true

   The CC shall be off when the Off button is pressed.

   The output ``cruiseState`` shall be set to ``OFF``.

.. hlr:: On
   :id: CC_HLR_CCB_04
   :collapse: true

   If the car speed is in the speed limit and the accelerator and brake pedals are not pressed,
   the CC shall be on and regulate the car speed.

   The output ``cruiseState`` shall be set to ``ON``.

.. hlr:: Stdby
   :id: CC_HLR_CCB_05
   :collapse: true

   The CC system shall be automatically off when the accelerator pedal is pressed, or the car speed is outside the speed limit.

   The output ``cruiseState`` shall be set to ``STDBY``.

.. hlr:: Not pressed
   :id: CC_HLR_CCB_06
   :collapse: true

   The system shall return to the ON state when both the accelerator pedal is not pressed,
   and the car speed is inside the speed limits.

   The output ``cruiseState`` shall be set to ``ON``.

.. hlr:: Brake
   :id: CC_HLR_CCB_07
   :collapse: true

   The CC shall be immediately interrupted when the brake is pressed.

   The output ``cruiseState`` shall be set to ``INT``.

.. hlr:: Resume
   :id: CC_HLR_CCB_08
   :collapse: true

   The system shall resume either to the ``ON`` or ``STDBY`` states,
   depending on the accelerator pedal and the speed value when the resume button is pressed.
