# Shared-parent paired-restriction encoding

## Question

Can one 26-gate AND/OR/NOT parent compute the full Heawood edge function while
the same gate operations and operands realize both restrictions at a
representative point input?

`synth_shared_parent_L_meta_9753.py` encodes exactly one parent. Its operation,
left-operand, and right-operand selectors are allocated once and shared by
every sampled row. Each sampled assignment is inserted together with its
`x0 = 0` or `x0 = 1` mate. No cofactor receives an independently minimized
gate list.

The encoding is counterexample-guided. A model is replayed on all 16,384 input
assignments. Any failing assignment returns to the example set together with
its restriction mate.

This tests shared-parent compatibility. It does not yet impose a syntactic
certificate that each restriction drops exactly three gates; the balanced
`(3,3)` equality case remains a separate structural condition.

## Reproduce the first paired instance

```sh
python3 sat/synth_shared_parent_L_meta_9753.py \
  init /tmp/L-meta-9753-shared-parent-examples.json
python3 sat/synth_shared_parent_L_meta_9753.py \
  encode /tmp/L-meta-9753-shared-parent-examples.json \
  /tmp/L-meta-9753-shared-parent.cnf 1
```

The pinned first-instance hashes are:

```text
examples  95e232dbe9adf62c7702f27e0f389f504eed12d10661cb4aa55068c81815b3bf
CNF       e4a292d03c158626708063770a5f0fa0b24a1995f4b3a8ab0b8ce290901cb35c
```

Optional arguments fix an exact NOT count and then a NOT position:

```sh
python3 sat/synth_shared_parent_L_meta_9753.py encode EXAMPLES CNF 1
python3 sat/synth_shared_parent_L_meta_9753.py encode EXAMPLES CNF 1 POSITION
```

## Symmetry boundaries already measured

Safe search reductions in this encoder are global parent reductions:

- order commutative gate operands canonically;
- require every non-output gate to be used; and
- optionally fix one global NOT count or position.

The following stronger assumptions have already failed or remain unsupported:

- **Independent cofactor minimization:** the known 27-gate teacher reduces to
  `23 | 26` at every point input, not a native shared `23 | 23` lineage.
- **Simple palindromic matrix symmetry:** natural, alternating, reversed, and
  palindromic point orders share the same measured matrix maximum.
- **Literal one-gate return:** all 729 delete-and-rewire returns were replayed;
  best distance was 47.
- **Frozen local three-gate repair:** every chain or fork of at most three
  AND/OR/NOT gates over all 28 earlier signals was exhausted; the exact result
  was `UNSAT` on three machines.

The distance-47 residue is localized: deleting gate 15 and returning to gate
14 omits exactly one point-line corner, and its 47 errors are exactly the
assignments where that edge is the unique witness. This does not exclude a
joint rewrite beginning earlier in the parent.

## Quantifier discipline

Whenever a reduction uses calibration names, probes, or sensors, the objects
must be chosen before the unknown key is evaluated, and their complete joint
answer map must be proved injective on the admissible key family. Pairwise
distinct names alone do not establish separation. No probe may be selected
after observing the answer it is meant to identify.
