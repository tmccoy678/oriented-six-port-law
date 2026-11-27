#!/usr/bin/env python3
"""Run the exact 512-assignment, 5,120-gate-evaluation local check."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: Path) -> list[list[int]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("{")]
    if not rows or not isinstance(rows[-1].get("gates"), list):
        raise ValueError("missing decoded gate list")
    gates = rows[-1]["gates"]
    if len(gates) != 10:
        raise ValueError("expected exactly ten local gates")
    return gates


def target(bits: list[bool]) -> bool:
    return (
        bits[0] and (bits[3] or bits[4] or bits[6])
    ) or (
        bits[1] and (bits[3] or bits[5] or bits[7])
    ) or (
        bits[2] and (bits[4] or bits[5] or bits[8])
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_intrinsic_local_witness.py LOCAL_JSON", file=sys.stderr)
        return 64
    gates = load(Path(sys.argv[1]))
    errors = 0
    evaluations = 0
    for assignment in range(1 << 9):
        wires = [bool((assignment >> wire) & 1) for wire in range(9)]
        for op, left, right in gates:
            if left >= len(wires) or right >= len(wires):
                raise ValueError("gate reads a future or missing wire")
            if op == 0:
                value = wires[left] and wires[right]
            elif op == 1:
                value = wires[left] or wires[right]
            elif op == 2:
                value = not wires[left]
            else:
                raise ValueError("unknown gate operation")
            wires.append(value)
            evaluations += 1
        errors += int(wires[-1] != target(wires[:9]))
    result = {
        "assignments": 512,
        "gates_per_assignment": 10,
        "gate_evaluations": evaluations,
        "errors": errors,
        "verdict": "ACCEPT" if errors == 0 else "REJECT",
    }
    print(json.dumps(result, separators=(",", ":")))
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
