# Research note: the centered `3,1,2` strand

Status: **active hypothesis, measured but unproved**.

## Recovered observation

The archived strand began with

```text
1, 4, 5, 7
```

and the provisional gap word `3,1,2`. Reading the continuation as an up/down
mirror gives

```text
terms: 1, 4, 5, 7, 9, 10, 13
gaps:  3, 1, 2, 2, 1, 3
```

The signed differences of the gaps are

```text
-2, +1, 0, -1, +2
```

and their magnitudes are

```text
2, 1, 0, 1, 2.
```

The central `2,2` is therefore a zero-change carrier between two mirrored
halves.

Modulo seven, the seven terms are

```text
1, 4, 5, 0, 2, 3, 6,
```

a complete ordering of the seven residues.

## Why it returned

The live proof target `L-meta-9753` is the edge function of the 14-vertex
Heawood graph, the incidence graph of the Fano plane: seven points, seven
lines, and 21 incidences. The known circuit has 27 gates; the open row asks for
26. A one-gate saving could arise if two mirrored computation cones read one
central carrier built once.

This is the gate-level analogue suggested by the proved relation

```text
M T M = T^-1.
```

## Controls already run

The palindromic point order was tested against the 7 by 7 incidence matrix.

- obvious same/reversed line orders: 21 of 49 mirrored cells;
- exhaustive best line ordering: 35 of 49;
- natural, alternating and reversed point-order controls: the same 35 of 49,
  with 288 maximizing line orders each.

Therefore simple matrix centrosymmetry does not distinguish the strand.

## Targeted solver test

Twenty-one one-edge-short 26-gate starting circuits were rebuilt in the
palindromic point order

```text
1, 4, 5, 0, 2, 3, 6.
```

Two independent Pro branches use restart seeds `312213` and `213312`. Both
began at distance 47 and reached distance 36, equal to the best natural-order
plateau at the recorded snapshot.

## Three-orientation closure

A distance-36 candidate was extracted and replayed on all 16,384 inputs.

- all 36 errors are false positives;
- the Hamming-weight multiplicities are mirror-symmetric;
- intersecting the error set with its point/line transpose leaves 18 cells;
- all 168 Fano-plane automorphisms were enumerated;
- 54 third orientations eliminate the remaining 18 cells; and
- the simplest uses point shift `i -> i + 1` and line shift `j -> j - 1`
  modulo seven.

Thus the measured identity is

```text
E(C) intersect E(C^T) intersect E(C_(+1,-1)) = empty.
```

The exact three-orientation consensus was generated as a fan-in-two network
and independently checked equivalent to the target on every input. Its raw
size is 80 gates. Logic synthesis reached 30 gates; the required public witness
is 26 gates.

The arithmetic reductions observed in the search are

```text
36 = 6 * 6
18 = 6 * 3
6 - 2 * 3 = 0.
```

Their established content is the measured 36-to-18-to-zero error-set closure.
The remaining theorem problem is to absorb the consensus into four fewer gates.

## The 25 + 1 frontier

The known exact 27-gate circuit ends with one OR activation gate. The shared
two-output body before it has 26 gates, and standard synthesis leaves that body
at 26. Therefore the public 26-gate theorem is equivalent to finding

```text
one shared 25-gate return body + one final activation gate.
```

This gives the earlier founder-frontier observation `25 = 5^2` a precise search
role. It remains a topology hypothesis: the arithmetic does not itself prove a
gate bound.

Controls:

- all 729 one-gate deletion/earlier-wire returns from the exact 27-gate circuit
  were replayed; best distance 47;
- greedy return-pruning of the exact 30-gate consensus to 26 gates produced
  distance 194; and
- standard multi-output synthesis leaves the exact pre-output body at 26 gates.

A targeted seed-25 branch now locks gate 26 as the final OR, mutates the shared
25-gate body and activation inputs, uses the palindromic point order, and starts
from the one-edge-short family. Its initial distance is 47.

## Falsification criterion

The strand earns a circuit role when a palindromic-order branch either:

1. improves below distance 36 on the frozen 16,384-row truth table; or
2. yields an exact 26-gate witness that independently replays on every input
   and compiles through the Lean checker.

Until then it remains a precise search-order hypothesis rather than a theorem.
