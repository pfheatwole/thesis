Data Preparation
================

.. todo::

   Discuss the data I will use (IGC tracks), its limitations, and how I plan to
   mitigate those limitations.


Variometer Debiasing
--------------------

Vario debiasing via dynamic time warping.

Talking points:
 * How GPS lags the variometer
   
 * How GPS lag causes a smoothing effect

 * How altitude pressure introduces a bias with changing altitude

 * Determing the vario bias from the two tracks

 * Issues with aligning the two sequences


Position Filtering
------------------

Kalman filter lat/lng/alt
