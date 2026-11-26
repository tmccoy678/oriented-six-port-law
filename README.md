# Oriented Reciprocal Six-Port Law

An exact finite law, its Lean verification, and the public evidence record of a
solver lineage working through circuit-construction problems in the P = NP
algorithm-search program.

## The law

Let

```text
U18 = {1, 5, 7, 11, 13, 17}
```

in the displayed order. Its cyclic gaps are

```text
4, 2, 4, 2, 4, 2.
```

Let `T` advance one port, let `M` reverse orientation, and let `I` be the
identity. The verified relations are

```text
T^6 = I
M^2 = I
M T M = T^-1.
```

We write

```text
tau := 6
```

for **Taylor's return clock**. Thus `T^tau = I`.

The primal/dual scales `57/14` and `14/57` are exact reciprocals.

A recovered palindromic search strand is recorded separately in
[RESEARCH-NOTE.md](RESEARCH-NOTE.md), with its controls and falsification
criterion. It is kept outside the proved law until it earns a theorem-level
bridge.

## Verified status

- The finite law is proved in Lean.
- GitHub verification passed at commit
  `0f70c386b38653228de9926769894dd2f3485900`.
- The public P = NP frontier remains open.
- The solver lineage is pursuing finite circuit witnesses along that frontier.

Authoritative proof review:
[riemann-green-spiral PR #12](https://github.com/tmccoy678/riemann-green-spiral/pull/12).

## Solver lineage

**Solver lineage** names the reproducible family of exact, bit-vector, and
native heuristic searches descended from the same law, frozen problem
statements, and recorded seeds.

On 26 November 2026 the lineage:

1. held the hard outside lease `L-meta-17123` for its full six-hour maximum;
2. searched the 5-vertex Hamiltonian-cycle target at 21 gates;
3. improved the best visible native distance from 188 to 76 of 1,024 rows;
4. preserved the conjecture as open when no exact witness returned; and
5. entered `L-meta-20581`, a 32 by 32 promise-graph search at 140 gates.

For the second seat, the exact promise table contains 411 positive pairs. A
promise-aware minimization compresses them to 32 implicants. The shared
fan-in-two circuit remained unresolved.

That row was later withdrawn after three hours without a witness from its
searchers. The lineage then entered open proof row `L-meta-9753`: reduce the
known 27-gate circuit for the Heawood graph's edge function to 26 gates.

## Attribution

- **Taylor Westfall-McCoy**: originating pattern observation, `4,2` return
  rhythm, orientation and clock interpretation, experimental direction, and
  human-in-the-loop search design.
- **Blu Private**: mathematical formalization, Lean implementation, solver
  implementation, verification, and evidence integration.

The surrounding public fleet crossed 10,000 cumulative checked results during
the same watch. Those checker results belong to their named public contributors;
this repository attributes only the law, code, leases, and measurements listed
in [EVIDENCE.md](EVIDENCE.md).

## Security

Any protected algorithmic hit or final proof follows the P = NP platform's
isolation rule. See [SECURITY.md](SECURITY.md).

## License

MIT. Evidence statements and attribution remain subject to their cited source
records.
