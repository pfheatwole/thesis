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

Example tasks:

* Sanitize the timestamps

* Check the GPS noise model (Chi^2 test)

* Debias the variometer data (via dynamic time warping or similar)

* Estimate atmospheric conditions (air density in particular)


[[I'd like to get some (small) amount of credit for the work I did on parsing
and cleaning the IGC code. I need to think about *how I present this work*.
I was thinking about putting it in an appendix, but the more I think about it,
the more I think it should go up front.

Start the paper by showing what data is available in an normal IGC track.
Time, latitude, longitude, pressure altitude, and GNSS altitude. Discuss the
limitations of that data (no sensor characteristics, etc), and summarize what
you can reasonably output.

**Establishing the nominal output from a normal IGC track sets up the rest of
the work!** Highlighting the nominal output shows what you have to work with
for the purposes of recreating the wind field for a given track. (Remember,
building a regression model over a single wind field is different from
extracting patterns from a *set* of wind fields.)]]
