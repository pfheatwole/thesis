*********************
Flight Reconstruction
*********************

.. Meta:

   * FIXME: starting from scratch


.. Informal overview (conversational definition of the problem)

* [[Start with a description of a pilot standing on the ground, looking up at
  a paraglider. They can use their knowledge of paraglider performance to
  ballpark the wind conditions up near the paraglider. We need to encode that
  knowledge in a mathematical model, and teach a computer to do the same
  estimation process.]]

* [[Build intuition for the model-based method by giving a "conversational"
  walk-through of how a pilot might estimate the wind by watching a glider.
  They're using domain knowledge; the program should do the same.

  In essence, that "intuitive" solution is simulating flights. They're doing
  flight reconstruction in their head.

  The new goal is to quantify a pilot's "intuitive" knowledge in mathematical
  form. The mathematical form enables statistical filtering methods that can
  combine the knowledge with our data to get what we want.]]



Conclusions:

* I know you can produce an estimate; the question is how precise it can be
  while remaining reasonably accurate.
