***********
Flight Data
***********

Key Points:

* In order to perform flight reconstruction on actual flights, you need to
  parse, clean, and transform the IGC data into the format required by the
  dynamics model.

* The output from this stage is the only parts of the flight that were
  observed; everything else must be simulated. The extreme limitations of this
  data establishes the constraints for the flight reconstruction stage.


* The fact that older tracks were inaccurate shouldn't mean we can't prepare
  for the continuing collection of new tracks! Newer GPS devices are getting
  very accurate; why not start designing for them?


Example tasks:

* Sanitize the timestamps

* Check the GPS noise model (Chi^2 test)

* Debias the variometer data (via dynamic time warping or similar)

* Estimate atmospheric conditions (air density in particular)
