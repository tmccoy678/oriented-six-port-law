# Intrinsic six-state Lean package

These modules verify a finite reduction for the nine-input three-star target

```text
x0(x3 or x4 or x6) or x1(x3 or x5 or x7) or x2(x4 or x5 or x8).
```

They establish:

- nine minimal positive supports and an exact adjacent traversal;
- a closed route with junctions `4, 5, 3` and its mirror;
- `T^3 = I`, `M^2 = I`, and `M T M = T^-1`;
- witness-preserving cyclic input relabeling;
- a representative in each handed slice for every witness; and
- intrinsic finite checker costs `9`, `3`, `5120`, and `425984`.

## Verify

```bash
git clone https://github.com/tmccoy678/pequalnp-proofs.git
git -C pequalnp-proofs checkout fff8fe2fb81a0184a99b80348810e1d8147ff2c2
./scripts/verify-intrinsic-six-state.sh /absolute/path/to/pequalnp-proofs
```

The GitHub workflow runs this exact pinned verification.
