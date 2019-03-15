.. FIXME: the first appendix needs to explicitly add `\appendix`

.. raw:: latex

    \appendix

***************
Data Processing
***************

Given a working particle filter, you can perform flight reconstruction on
actual flights. But first you need to parse and sanitize the flight data.


* Sanitize the timestamps

* Check the GPS noise model (Chi^2 test)

* Debias the variometer data (via dynamic time warping or similar)

* Estimate atmospheric conditions (air density in particular)
