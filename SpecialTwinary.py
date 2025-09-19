"""
Twinary number system experiment.

Toby gave me a number system called "twinary." 
Numbers are written in base 3, but instead of coefficients {0,1,2}, 
the "digits" are either 0 or a power of 2.  

The question: can every integer be represented in this system such that 
the powers of two strictly descend as the powers of three increase?

This script uses PyTorch for parallelism to explore the construction.
"""

import torch
from itertools import combinations

# --------------------------------------------
# Setup
# --------------------------------------------
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

n = 6                      # number of ternary positions
m = 2 ** n                 # number of binary masks (all subsets of {1,...,n})

# --------------------------------------------
# Step 1. Generate all subsets of {1,...,n}
# --------------------------------------------
ran = torch.arange(m, device=device)

# Binary representation of subsets: shape (m, n)
bin_rep = ((ran.unsqueeze(1) & (1 << torch.arange(n, device=device))) > 0).to(torch.int8)

# Convert to index representation (0 where absent, otherwise position+1)
indices = torch.arange(1, n + 1, device=device)
subsets = bin_rep * indices  # (m, n)

# --------------------------------------------
# Step 2. Pad each subset in all possible ways
# --------------------------------------------
padded_subsets = []

for l in range(n + 1):
    # Select all subsets of size l
    mask = (subsets != 0).sum(1) == l
    if not mask.any():
        continue

    these = subsets[mask]

    if l == 0:
        # The empty subset -> just one zero vector
        zeros = torch.zeros((len(these), 1, n), dtype=torch.int8, device=device)
        padded_subsets.append(zeros)
        continue

    # Non-empty subsets of size l
    these_vals = these[these != 0].reshape(-1, l)  # (#subsets, l)

    # All ways to place l entries in length-n vector
    positions = torch.tensor(list(combinations(range(n), l)), device=device)  # (#positions, l)

    # Expand to match (#subsets, #positions, l)
    expanded_vals = these_vals.unsqueeze(1).expand(-1, len(positions), -1).to(torch.int8)
    expanded_pos = positions.unsqueeze(0).expand(len(these_vals), -1, -1)

    # Scatter values into zero-padded slots
    out = torch.zeros((len(these_vals), len(positions), n), dtype=torch.int8, device=device)
    out.scatter_(2, expanded_pos, expanded_vals)

    padded_subsets.append(out)

# Flatten to a single (num_variants, n) tensor
padded_subsets = torch.cat([x.reshape(-1, n) for x in padded_subsets], dim=0)

# --------------------------------------------
# Step 3. Compute weighted sums with powers of 2 and 3
# --------------------------------------------
powers_of_3 = 3 ** torch.arange(n, device=device)          # increasing powers of 3
powers_of_2 = 2 ** torch.arange(n - 1, -1, -1, device=device)  # decreasing powers of 2

# Outer product gives (n, n) matrix of all 3^i * 2^j
outer = torch.outer(powers_of_3, powers_of_2)

# Mask nonzero entries in subsets
mask = padded_subsets > 0
row_idx = torch.arange(n, device=device).unsqueeze(0).expand(padded_subsets.size(0), -1)
col_idx = (padded_subsets - 1).clamp(min=0).to(torch.long)

# Gather contributions and sum
selected = outer[row_idx, col_idx] * mask
sums = selected.sum(dim=1)

# Sort by numeric value
perm = torch.argsort(sums)
results = sums.tolist()
print("Sorted Results:", [results[i] for i in perm])

# --------------------------------------------
# Step 4. Express sorted subsets as exponents of 2
# --------------------------------------------
sorted_subsets = padded_subsets[perm]

# Replace 0 with -inf; nonzero x → exponent n-x
sorted_exponents = torch.where(sorted_subsets == 0, float('-inf'), n - sorted_subsets)
print("Sorted Exponents:", sorted_exponents.tolist())
