*********************
Wind Field Prediction
*********************

Key Points:

* A predictive model uses the correlated spatial regions to respond to
  queries. Given a set of wind vector estimates (given as a batch or
  individually), use the spatial correlations to build a estimate of the
  highly correlated regions.

* How do you handle the spatiotemporal averaging? In terms of time, do you
  group observations by a sliding 1-hour window, etc? In terms of space, do
  you use a continuous regression model or do you use a grid?



Model Encoding
==============

To be useable using an in-flight device with no access to cellular network,
the model must be self-contained, and it must meet the storage and computation
constraints of a low-power embedded device. How the model is encoded is
fundamental to how it is queried. [[Is it though? On-disk encoding isn't
necessarily the same as the in-memory representation; granted though, the
advantage of what I was doing was to make the on-disk model be compact and
directly queriable without loading it into memory.]]
