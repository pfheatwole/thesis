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
   * - :math:`\vec{x}^c`
     - a vector in the coordinate system :math:`c`
   * - :math:`\vec{x}_{B/A}`
     - a vector from point A to point B (point B with respect to point A)
   * - :math:`{^r \dot{\vec{x}}}`
     - the derivative of a vector taken in reference frame
       :math:`\mathcal{F}_r`
   * - :math:`x_k`
     - a variable at index :math:`k` of a sequence of length :math:`K`
   * - :math:`x^{(n)}`
     - element :math:`n` of a set of :math:`N` elements
   * - :math:`\mat{X}_{M \times N}`
     - a matrix with :math:`M` rows and :math:`N` columns
   * - :math:`\mat{X}^z`
     - a matrix exponential, where :math:`z` is a scalar
   * - :math:`\left| x \right|`
     - absolute value of a scalar
   * - :math:`\left\| \vec{x} \right\|`
     - Euclidean norm of a vector
   * - :math:`\left| \mat{X} \right|`
     - determinant of a matrix
   * - :math:`\mat{C}_{b/a}`
     - the directed cosine matrix that transforms vectors from coordinate
       system :math:`a` into coordinate system :math:`b`
   * - :math:`\vec{q}_{b/a}`
     - a quaternion that encodes the relative orientation of coordinate system
       :math:`b` relative to coordinate system :math:`a`
   * - :math:`\vec{\omega}_{b/a}`
     - angular velocity vector of frame :math:`\mathcal{F}_b` with respect to frame
       :math:`\mathcal{F}_a`
   * - :math:`f(\cdot)`, :math:`func(\cdot)`, etc
     - functions, where ``f``, ``func``, can be any identifier
   * - :math:`p(\cdot)`
     - a probability density function. This identifier is unique because it
       can be used many times for different density functions. For example,
       :math:`p(x)` and :math:`p(y)` are different functions even though both
       use :math:`p`.

Another notation which is useful when building systems of equations involving
matrices is the *cross-product matrix operator*, so that
:math:`\crossmat{\vec{v}} \vec{x} \equiv \vec{v} \times \vec{x}`:

.. _crossmat:
.. math::

   \crossmat{\vec{v}} \defas
      \begin{bmatrix}
         0 & -v_3 & v_2\\
         v_3 & 0 & -v1\\
         -v_2 & v_1 & 0
      \end{bmatrix}

.. FIXME:

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
   \vec{p}_{A/B} &\defas
      \text{the position of the point A with respect to point } B \\
   \vec{v}_{A/i} &\defas
      \text{the velocity vector of a point } A \text{ in frame } \mathcal{F}_i \\
   ^b \dot{\vec{v}}_{A/i} &\defas
      \text{the vector derivative of } \vec{v}_{A/i} \text{ taken in frame } \mathcal{F}_b \\
   \vec{v}^c_{A/i} &\defas
      \text{array of components of } \vec{v}_{A/i} \text{ in coordinate system } c \\
   ^b \dot{\vec{v}}^c_{A/i} &\defas
      \text{components in coordinate system } c \text{ of the derivative taken in frame } \mathcal{F}_b
   \end{aligned}
