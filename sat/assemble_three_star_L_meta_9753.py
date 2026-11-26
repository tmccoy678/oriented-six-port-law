#!/usr/bin/env python3
"""Expand a verified 10-gate three-star return cell into the 26-gate L-meta-9753 circuit."""

from __future__ import annotations

import json
import sys
from pathlib import Path


LOCAL_INPUTS = [0, 1, 6, 7, 8, 9, 10, 13, 11]
NEIGHBORS = {
    2: [8, 12, 13],
    3: [7, 11, 12],
    4: [10, 11, 13],
    5: [9, 10, 12],
}
EDGES = [
    (0, 7), (0, 8), (0, 10), (1, 7), (1, 9), (1, 13),
    (2, 8), (2, 12), (2, 13), (3, 7), (3, 11), (3, 12),
    (4, 10), (4, 11), (4, 13), (5, 9), (5, 10), (5, 12),
    (6, 8), (6, 9), (6, 11),
]


def load_local(path: Path) -> list[list[int]]:
    values = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("{")]
    if not values:
        raise ValueError("no local JSON circuit")
    gates = values[-1].get("gates")
    if not isinstance(gates, list) or len(gates) != 10:
        raise ValueError("local circuit must contain exactly 10 gates")
    return gates


def map_wire(wire: int) -> int:
    return LOCAL_INPUTS[wire] if wire < len(LOCAL_INPUTS) else 14 + wire - len(LOCAL_INPUTS)


def assemble(local: list[list[int]]) -> list[list[int]]:
    gates = [[op, map_wire(left), map_wire(right)] for op, left, right in local]
    terms = [23]
    for point in (2, 3, 4, 5):
        a, b, c = NEIGHBORS[point]
        gates.append([1, a, b])
        first = 14 + len(gates) - 1
        gates.append([1, first, c])
        cone = 14 + len(gates) - 1
        gates.append([0, point, cone])
        terms.append(14 + len(gates) - 1)
    output = terms[0]
    for term in terms[1:]:
        gates.append([1, output, term])
        output = 14 + len(gates) - 1
    if len(gates) != 26 or output != 39:
        raise AssertionError((len(gates), output))
    return gates


def evaluate(gates: list[list[int]]) -> tuple[int, int, int]:
    errors = false_positives = false_negatives = 0
    for assignment in range(1 << 14):
        wires = [bool((assignment >> wire) & 1) for wire in range(14)]
        for op, left, right in gates:
            if op == 0:
                wires.append(wires[left] and wires[right])
            elif op == 1:
                wires.append(wires[left] or wires[right])
            elif op == 2:
                wires.append(not wires[left])
            else:
                raise ValueError(f"bad op {op}")
        expected = any(wires[left] and wires[right] for left, right in EDGES)
        actual = wires[39]
        if actual != expected:
            errors += 1
            false_positives += int(actual and not expected)
            false_negatives += int(expected and not actual)
    return errors, false_positives, false_negatives


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} LOCAL_CIRCUIT_JSON", file=sys.stderr)
        return 64
    gates = assemble(load_local(Path(sys.argv[1])))
    errors, false_positives, false_negatives = evaluate(gates)
    print(f"assembled fitness={errors} false_positives={false_positives} false_negatives={false_negatives}")
    if errors:
        return 1
    counts = {
        "and": sum(gate[0] == 0 for gate in gates),
        "or": sum(gate[0] == 1 for gate in gates),
        "not": sum(gate[0] == 2 for gate in gates),
    }
    print("WITNESS three-star-return fitness=0")
    print(json.dumps({"gates": gates, "output": 39, "counts": counts, "fitness": 0}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
