#!/usr/bin/env python3
"""Exact SAT synthesis for the isolated 9-input, 10-gate three-star return cell."""

from __future__ import annotations

import json
import sys
from pathlib import Path


INPUTS = 9
GATES = 10
ASSIGNMENTS = 1 << INPUTS


class Variables:
    def __init__(self) -> None:
        self.next_id = 1
        self.op: list[list[int]] = []
        self.left: list[list[int]] = []
        self.right: list[list[int]] = []
        self.left_value: list[list[int]] = []
        self.right_value: list[list[int]] = []
        self.value: list[list[int]] = []
        for gate in range(GATES):
            limit = INPUTS + gate
            self.op.append(self.fresh(3))
            self.left.append(self.fresh(limit))
            self.right.append(self.fresh(limit))
        for _assignment in range(ASSIGNMENTS):
            self.left_value.append(self.fresh(GATES))
            self.right_value.append(self.fresh(GATES))
            self.value.append(self.fresh(GATES))

    def fresh(self, count: int) -> list[int]:
        result = list(range(self.next_id, self.next_id + count))
        self.next_id += count
        return result


def exactly_one(clauses: list[list[int]], variables: list[int]) -> None:
    clauses.append(variables)
    for index, left in enumerate(variables):
        for right in variables[index + 1 :]:
            clauses.append([-left, -right])


def input_bit(assignment: int, wire: int) -> bool:
    return bool((assignment >> wire) & 1)


def target(assignment: int) -> bool:
    bit = lambda wire: input_bit(assignment, wire)
    p = bit(0) and (bit(3) or bit(4) or bit(6))
    q = bit(1) and (bit(3) or bit(5) or bit(7))
    r = bit(2) and (bit(4) or bit(5) or bit(8))
    return p or q or r


def selected_value(
    clauses: list[list[int]],
    variables: Variables,
    assignment: int,
    gate: int,
    selectors: list[int],
    selected: int,
) -> None:
    for wire, selector in enumerate(selectors):
        if wire < INPUTS:
            clauses.append([-selector, selected if input_bit(assignment, wire) else -selected])
        else:
            source = variables.value[assignment][wire - INPUTS]
            clauses.append([-selector, -selected, source])
            clauses.append([-selector, selected, -source])


def build(tight: bool = False) -> tuple[Variables, list[list[int]]]:
    variables = Variables()
    clauses: list[list[int]] = []
    for gate in range(GATES):
        exactly_one(clauses, variables.op[gate])
        exactly_one(clauses, variables.left[gate])
        exactly_one(clauses, variables.right[gate])
        and_op, or_op, _not_op = variables.op[gate]
        for left_wire, left_selector in enumerate(variables.left[gate]):
            for right_wire, right_selector in enumerate(variables.right[gate]):
                if left_wire > right_wire:
                    clauses.append([-and_op, -left_selector, -right_selector])
                    clauses.append([-or_op, -left_selector, -right_selector])
                if tight and left_wire == right_wire:
                    clauses.append([-and_op, -left_selector, -right_selector])
                    clauses.append([-or_op, -left_selector, -right_selector])
                if tight and left_wire != right_wire:
                    clauses.append([-variables.op[gate][2], -left_selector, -right_selector])

    if tight:
        for source_gate in range(GATES - 1):
            source_wire = INPUTS + source_gate
            uses = []
            for consumer in range(source_gate + 1, GATES):
                uses.append(variables.left[consumer][source_wire])
                uses.append(variables.right[consumer][source_wire])
            clauses.append(uses)

    for assignment in range(ASSIGNMENTS):
        for gate in range(GATES):
            left = variables.left_value[assignment][gate]
            right = variables.right_value[assignment][gate]
            value = variables.value[assignment][gate]
            selected_value(clauses, variables, assignment, gate, variables.left[gate], left)
            selected_value(clauses, variables, assignment, gate, variables.right[gate], right)
            and_op, or_op, not_op = variables.op[gate]
            clauses.extend(
                [
                    [-and_op, -left, -right, value],
                    [-and_op, left, -value],
                    [-and_op, right, -value],
                    [-or_op, left, right, -value],
                    [-or_op, -left, value],
                    [-or_op, -right, value],
                    [-not_op, left, value],
                    [-not_op, -left, -value],
                ]
            )
        output = variables.value[assignment][GATES - 1]
        clauses.append([output if target(assignment) else -output])
    return variables, clauses


def encode(path: Path, tight: bool = False) -> int:
    variables, clauses = build(tight=tight)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {variables.next_id - 1} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(json.dumps({"variables": variables.next_id - 1, "clauses": len(clauses)}))
    return 0


def decode(path: Path) -> int:
    text = path.read_text(encoding="ascii", errors="replace")
    if "s UNSATISFIABLE" in text:
        print("UNSAT")
        return 20
    if "s SATISFIABLE" not in text:
        print("no SAT verdict", file=sys.stderr)
        return 2
    positive = {
        int(token)
        for line in text.splitlines()
        if line.startswith("v ")
        for token in line[2:].split()
        if token != "0" and not token.startswith("-")
    }
    variables = Variables()
    gates = []
    for gate in range(GATES):
        op = next(index for index, variable in enumerate(variables.op[gate]) if variable in positive)
        left = next(index for index, variable in enumerate(variables.left[gate]) if variable in positive)
        right = next(index for index, variable in enumerate(variables.right[gate]) if variable in positive)
        gates.append([op, left, right])
    print(json.dumps({"gates": gates, "output": INPUTS + GATES - 1, "fitness": 0}, separators=(",", ":")))
    return 0


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in {"encode", "encode-tight", "decode"}:
        print(f"usage: {Path(sys.argv[0]).name} encode CNF | encode-tight CNF | decode SOLVER_OUTPUT", file=sys.stderr)
        return 64
    if sys.argv[1] == "decode":
        return decode(Path(sys.argv[2]))
    return encode(Path(sys.argv[2]), tight=sys.argv[1] == "encode-tight")


if __name__ == "__main__":
    raise SystemExit(main())
