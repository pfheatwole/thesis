import numpy as np

alpha_min = -6
alpha_max = 22
K_alpha = (alpha_max - alpha_min) * 2 + 1

commands = [
    "oper",
    "o",  # Enter the options
    "r",  # Moments about the body axes
    "",
]

alphas = np.linspace(alpha_min, alpha_max, K_alpha)
# for beta in [0, 5, 10, 15]:
for beta in np.arange(-15, 16):
    commands.append(f"b b {beta}")
    for k, alpha in enumerate(alphas):
        commands.append(str(k+1))
        commands.append(f"a a {alpha}")
        commands.append("x")
        commands.append("w")
        commands.append(f"forces/beta{beta:02}_alpha{alpha:0.3f}.txt")

commands.append("")
commands.append("QUIT")

with open("commands.txt", "w") as f:
    for command in commands:
        f.write(command + "\n")
