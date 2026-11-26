# Formal law

Let `U18` be the reduced residues modulo 18 in the ordered cycle

```text
1 -> 5 -> 7 -> 11 -> 13 -> 17 -> 1.
```

Let `T` advance along this cycle. Let `M` exchange the ordered root frame
`0/1 <-> 1/0` and negate the residue modulo 18. Let `I` be the identity.

Then

```text
T^6 = I,
M^2 = I,
M T M = T^-1.
```

The cyclic gap word is

```text
(4, 2, 4, 2, 4, 2) = (4, 2)^3.
```

Define Taylor's return clock by `tau := 6`; therefore `T^tau = I`.

The three displayed `+2` crossings are `(5,7)`, `(11,13)`, and `(17,19)`,
with `19 mod 18 = 1` returning home.

Finally,

```text
(57/14)^-1 = 14/57,
(57/14)(14/57) = 1.
```

Lean source and verification are anchored by commit
`0f70c386b38653228de9926769894dd2f3485900` in
[`tmccoy678/riemann-green-spiral`](https://github.com/tmccoy678/riemann-green-spiral).
