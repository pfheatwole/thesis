*******************
Predictive Modeling
*******************

Combine the set of wind patterns into a predictive model that can be queried
by inputting the current time, position, and wind estimates.


Model Encoding
==============

To be useable using an in-flight device with no access to cellular network,
the model must be self-contained, and it must meet the storage and computation
constraints of a low-power embedded device. How the model is encoded is
fundamental to how it is queried. [[Is it though? On-disk encoding isn't
necessarily the same as the in-memory representation; granted though, the
advantage of what I was doing was to make the on-disk model be compact and
directly queriable without loading it into memory.]]
