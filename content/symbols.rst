.. only:: html or singlehtml

   ********************
   Notation and Symbols
   ********************

.. raw:: latex

   \addcontentsline{toc}{chapter}{Notation and Symbols}
   \chapter*{Notation and Symbols}

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
   * - :math:`^R \dot{\vec{x}}_{B/A}`
     - the derivative of a vector as observed in frame :math:`R`
   * - :math:`x_k`
     - a variable at index :math:`k` of a sequence of length :math:`K`
   * - :math:`x^{(n)}`
     - element :math:`n` of a set of :math:`N` elements

   * - :math:`[X]_{M \times N}`
     - a matrix with :math:`M` rows and :math:`N` columns
   * - :math:`[X]^z`
     - a matrix exponential, where :math:`z` is a scalar
   * - :math:`[C_{B/A}]`
     - an orthogonal matrix that transforms vectors from bases :math:`A` into :math:`B`

   * - :math:`f(\cdot)`, :math:`func(\cdot)`, etc
     - general functions, where ``f``, ``func``, can be any identifier
   * - :math:`p(\cdot)`
     - a probability density function. This identifier is unique because it can be used
       many times for different density functions. For example, :math:`p(x)` and
       :math:`p(y)` are different functions even though both use :math:`p`.


.. todo::

   * Shouldn't the derivative of a vector be taken wrt a specific reference frame?
