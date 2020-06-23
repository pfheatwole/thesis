import re

import numpy as np

alpha_min = -6
alpha_max = 22
K_alpha = (alpha_max - alpha_min) * 2 + 1
alphas = np.linspace(alpha_min, alpha_max, K_alpha)
floatre = r"tot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)"

for beta in np.arange(-15, 16):
    coefficients = "CX CY CZ CL CD Cl Cm Cn".split()
    values = {c: [] for c in coefficients}

    for alpha in alphas:
        with open(f"forces/beta{beta:02}_alpha{alpha:0.3f}.txt") as f:
            lines = "\n".join(f.readlines())
            for c in coefficients:
                match = re.search(str(c) + floatre, lines)
                values[c].append(float(match.group(1)))

    np.savetxt(
        f"beta{beta:02}.txt",
        np.stack([alphas, *[values[c] for c in coefficients]]).T,
        header=" ".join(["alpha", *coefficients]),
        fmt=["%.1f", *(["%.5f"] * len(coefficients))],
    )
