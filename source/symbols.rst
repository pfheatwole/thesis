********************
Notation and Symbols
********************

.. _common_notation:
.. list-table:: Common Notation
   :header-rows: 1
   :widths: 10 25
   :align: center

   * - Notation
     - Meaning
   * - :math:`x`
     - a scalar
   * - :math:`\vec{x}`
     - a vector
   * - :math:`x^y`
     - a scalar raised to a power, where :math:`y` is a scalar
   * - :math:`\vec{x}^C`
     - a vector in the coordinate system :math:`C`
   * - :math:`\vec{x}_{B/A}`
     - a vector from point A to point B (point B with respect to point A)
   * - :math:`^R \vec{x}`
     - a vector in reference frame :math:`R`
   * - :math:`\dot{\vec{x}}`
     - the derivative of a vector
   * - :math:`x_k`
     - a variable at index :math:`k` of a sequence of length :math:`K`
   * - :math:`x^{(n)}`
     - element :math:`n` of a set of :math:`N` elements

   * - :math:`\mat{X}_{M \times N}`
     - a matrix with :math:`M` rows and :math:`N` columns
   * - :math:`\mat{X}^z`
     - a matrix exponential, where :math:`z` is a scalar
   * - :math:`\mat{C_{B/A}}`
     - an orthogonal matrix that transforms vectors from bases :math:`A` into
       :math:`B`

   * - :math:`f(\cdot)`, :math:`func(\cdot)`, etc
     - functions, where ``f``, ``func``, can be any identifier
   * - :math:`p(\cdot)`
     - a probability density function. This identifier is unique because it
       can be used many times for different density functions. For example,
       :math:`p(x)` and :math:`p(y)` are different functions even though both
       use :math:`p`.

.. todo::

   Define random variables (eg, :math:`X`) and random variates (:math:`x
   \in X`). Most of my functions are developed in terms of deterministic
   variables, but later those variables will be considered random (so the
   functions are now defined in terms of random variates). Not sure if/how
   to call this out explicitly.

By their nature, vectors require the most intricate notation, since a fully
specified vector might include all of:

1. A reference frame

2. A coordinate system

3. A fixed point (if it's a bound vector)

For simplicity, :numref:`common_notation` only shows examples of each distinct
element of a vector encoding. In practice, vectors may appear quite complex;
for some realistic examples taken from
:cite:`stevens2015AircraftControlSimulation`:

.. math::

   \begin{aligned}
   \vec{p}_{A/B} &\equiv \textrm{the position of the point A with respect to point } B \\
   \vec{v}_{A/i} &\equiv \textrm{the velocity vector of a point } A \textrm{ in frame } F_i \\
   ^b \dot{\vec{v}}_{A/i} &\equiv \textrm{the vector derivative of } \vec{v}_{A/i} \textrm{ taken in frame } F_b \\
   \vec{v}^C_{A/i} \equiv \left(\vec{v}_{A/i}\right)^C &\equiv \textrm{array of components of } \vec{v}_{A/i} \textrm{ in coordinate system } c \\
   ^b \dot{\vec{v}}^c_{A/i} &\equiv \textrm{components in coordinate system } c \textrm{ of the derivative taken in frame } F_b
   \end{aligned}
