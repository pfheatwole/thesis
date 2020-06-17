import re

import numpy as np

from IPython import embed

alpha_min = -6
alpha_max = 22
K_alpha = (alpha_max - alpha_min) * 2 + 1
alphas = np.linspace(alpha_min, alpha_max, K_alpha)

# for beta in [0, 5, 10, 15]:
for beta in np.arange(-15, 16):
    # Wasteful as heck, but who cares
    CXs, CYs, CZs = [], [], []
    CLs, CDs = [], []
    Cls, Cms, Cns = [], [], []
    for alpha in alphas:
        with open(f"forces/beta{beta:02}_alpha{alpha:0.3f}.txt") as f:
            lines = f.readlines()

            for line in lines:
                match = re.match(r"  CXtot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    CXs.append(float(match.group(1)))
                    break

            for line in lines:
                match = re.match(r"  CYtot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    CYs.append(float(match.group(1)))
                    break

            for line in lines:
                match = re.match(r"  CZtot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    CZs.append(float(match.group(1)))
                    break

            # ---------------------------------------------------------------

            for line in lines:
                match = re.match(r"  CLtot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    CLs.append(float(match.group(1)))
                    break

            for line in lines:
                match = re.match(r"  CDtot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    CDs.append(float(match.group(1)))
                    break

            # ---------------------------------------------------------------

            for line in lines:
                match = re.search(r" Cltot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    Cls.append(float(match.group(1)))
                    break

            for line in lines:
                match = re.search(r" Cmtot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    Cms.append(float(match.group(1)))
                    break

            for line in lines:
                match = re.search(r" Cntot =\s*([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)", line)
                if match is not None:
                    Cns.append(float(match.group(1)))
                    break

    np.savetxt(
        f"beta{beta:02}.txt",
        np.c_[alphas, CXs, CYs, CZs, CLs, CDs, Cls, Cms, Cns],
        header="alpha CX CY CZ CL CD Cl Cm Cn",
        fmt=["%.1f", *(["%.5f"] * 8)],
    )
