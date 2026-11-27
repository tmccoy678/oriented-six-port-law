#!/usr/bin/env python3
"""Add one internal handedness bit to the unrestricted three-star CNF."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


EXPECTED_SOURCE = "c903f0cc36f4678ebe2eb8bc156d4225d7c88e19958dac117d331d67e304cdd9"
EXPECTED_HEADER = "p cnf 15660 229392"
HAND = 15661
RIGHT = [4, 7, 10, 13, 16, 19]
LEFT = [4, 8, 10, 13, 17, 19]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: build_intrinsic_six_state_cnf.py SOURCE OUTPUT RECEIPT", file=sys.stderr)
        return 64
    source, output, receipt = map(Path, sys.argv[1:])
    if sha256(source) != EXPECTED_SOURCE:
        raise SystemExit("refused: unrestricted source CNF hash mismatch")
    if output.exists() or receipt.exists():
        raise SystemExit("refused: output already exists")

    lines = source.read_text(encoding="ascii").splitlines()
    header = next((i for i, line in enumerate(lines) if line.startswith("p cnf ")), None)
    if header is None or lines[header] != EXPECTED_HEADER:
        raise SystemExit("refused: unexpected DIMACS header")
    lines[header] = "p cnf 15661 229394"
    right = [-HAND] + RIGHT
    left = [HAND] + LEFT
    lines.append(" ".join(map(str, right)) + " 0")
    lines.append(" ".join(map(str, left)) + " 0")
    output.write_text("\n".join(lines) + "\n", encoding="ascii")

    record = {
        "source_cnf_sha256": EXPECTED_SOURCE,
        "derived_cnf_sha256": sha256(output),
        "variables": 15661,
        "clauses": 229394,
        "hand_variable": HAND,
        "right_conditional_clause": right,
        "left_conditional_clause": left,
        "check_contracts": {
            "node_route_steps": 9,
            "orientation_steps": 3,
            "local_witness_gate_evaluations": 5120,
            "full_witness_gate_evaluations": 425984,
        },
    }
    receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
