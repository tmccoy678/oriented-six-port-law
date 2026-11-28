# Frozen three-star return synthesis

This directory records the exact finite synthesis instance placed into CaDiCaL
before its verdict. It is the local compression frontier for proof row
`L-meta-9753`.

## Derivation

The measured 26-gate near-circuit has 36 errors, all false positives. Exhaustive
replay separates them into two disjoint sets:

```text
forbidden pair (6, 7): 18
forbidden pair (1, 8): 18
overlap:                 0
```

Both defects lie in one three-star return cell. With local inputs
`p, q, r, a, b, d, c, e, f`, its exact target is

```text
p & (a | b | c) |
q & (a | d | e) |
r & (b | d | f).
```

The ordinary realization takes 11 gates. The frozen SAT instance asks for an
exact 10-gate AND/OR/NOT circuit. Such a cell would assemble the full witness as

```text
10-gate return cell + 12 untouched star gates + 4 joins = 26 gates.
```

## Frozen instance

The frozen pre-result instance uses the `encode-tight` normal form:

```text
variables: 15,660
clauses:   231,441
CNF SHA-256: 93259dc4c97f3291d8e59f94ddf759d7d5d8131d13517de002ecaf6c63beba6c
solver: CaDiCaL 2.1.2
```

`encode-tight` requires every gate to be used, excludes idempotent AND/OR gates,
and canonicalizes the unused second input of NOT. A SAT model is a valid witness
regardless of these search restrictions. An UNSAT result for this normal form
does not by itself settle the unrestricted `encode` instance.

The construction was published before a solver verdict at
`2026-11-26T23:53:27Z`.

## Reproduce

Generate the byte-identical tight instance:

```bash
python3 sat/synth_three_star_return_sat.py encode-tight /tmp/L_meta_9753_three_star_tight.cnf
shasum -a 256 /tmp/L_meta_9753_three_star_tight.cnf
```

Run it with CaDiCaL and assemble any SAT model:

```bash
sat/run-tight.sh /path/to/cadical
```

The assembler independently replays all 16,384 assignments of the full
14-input target. It emits a witness only at zero error. The repository workflow
regenerates the CNF and checks its frozen hash on every commit.

## Intrinsic six-state instance

Generate the unrestricted source and add one internal handedness bit:

```bash
python3 sat/synth_three_star_return_sat.py encode /tmp/three-star-unrestricted.cnf
python3 sat/build_intrinsic_six_state_cnf.py \
  /tmp/three-star-unrestricted.cnf \
  /tmp/intrinsic-six-state.cnf \
  /tmp/intrinsic-six-state.json
```

The hand variable conditionally selects one of two Lean-proved representative
slices. It changes no target clause. The expected derived hash is

```text
51fac531f709e1eb2d64c3a0a0958618f27f0e1b76047ded204cb7d9525e48e7
```

For any decoded ten-gate model, run the fixed local checker before assembly:

```bash
python3 sat/verify_intrinsic_local_witness.py /path/to/local-model.json
```

It performs exactly 512 assignments times ten gates: 5,120 gate evaluations.

## Files

- `synth_three_star_return_sat.py`: deterministic unrestricted and tight CNF
  encoders, plus CaDiCaL model decoder.
- `assemble_three_star_L_meta_9753.py`: deterministic 10-to-26 gate expansion
  and exhaustive full-target evaluator.
- `run-tight.sh`: relative end-to-end runner.
- `build_intrinsic_six_state_cnf.py`: deterministic two-handed reduction.
- `verify_intrinsic_local_witness.py`: exact 5,120-evaluation local checker.
- `instance-manifest.json`: machine-readable frozen-instance record.
