Car driving control
===================

.. hlr:: Off
   :id: CC_HLR_CDC_01
   :collapse: true

   When the CC is off, the car speed shall be driven using the accelerator pedal.

.. hlr:: On
   :id: CC_HLR_CDC_02
   :collapse: true

   When the CC is on, the car speed shall be automatically regulated.

.. hlr:: PI
   :id: CC_HLR_CDC_03
   :collapse: true

   The regulation shall be done using a proportional and integral algorithm, with ``KP`` and ``KI`` factors.

.. hlr:: Protection
   :id: CC_HLR_CDC_04
   :collapse: true

   The regulation algorithm shall be protected against the overshoot of its integral part:
   the integral action shall be reset when the CC is going on, and frozen when the throttle output is saturated.

.. hlr:: Saturation
   :id: CC_HLR_CDC_05
   :collapse: true

   The throttle command shall be saturated at ``THROTTLE_SAT_MAX`` when automatically regulating,
   to limit the car acceleration for the comfort.
