#!/usr/bin/env python3
"""Shared-parent counterexample-guided synthesis for L-meta-9753.

One global set of 26 gate operation and operand selectors defines the parent.
Every sampled assignment is paired at input x0, so both restrictions are
evaluated against those identical parent choices. Each SAT model is replayed
on all 2^14 inputs; a failing assignment and its restriction mate are appended
together.

This encodes the shared parent requested in the balanced (3,3) investigation.
It does not assert syntactic gate drops of exactly three on either restriction;
that equality case still requires a witness or a separate structural encoding.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


INPUTS = 14
GATES = 26
RESTRICTION_INPUT = 0
Q5_INPUT_COLUMNS = [
    95229015649943559,
    63038587666488,
    256462815680,
    4292497062759936,
    8521481482240,
    14003410187812864,
    55389823207997440,
    189297016294081033,
    155696362464477250,
    218994303132270608,
    183565875465490436,
    229736628138025984,
    270286071508633728,
    288160007407550752,
]
Q5_TARGET = 2097151
EDGES = [
    (0, 7), (0, 8), (0, 10),
    (1, 7), (1, 9), (1, 13),
    (2, 8), (2, 12), (2, 13),
    (3, 7), (3, 11), (3, 12),
    (4, 10), (4, 11), (4, 13),
    (5, 9), (5, 10), (5, 12),
    (6, 8), (6, 9), (6, 11),
]


class Variables:
    def __init__(self, example_count: int) -> None:
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
        for _ in range(example_count):
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
        for right in variables[index + 1:]:
            clauses.append([-left, -right])


def target(assignment: int) -> bool:
    return any((assignment >> left) & 1 and (assignment >> right) & 1
               for left, right in EDGES)


def paired_assignments(values: list[int]) -> list[int]:
    """Freeze the representative input and retain both restriction mates."""
    bit = 1 << RESTRICTION_INPUT
    paired = []
    for assignment in values:
        base = assignment & ~bit
        paired.extend((base, base | bit))
    return list(dict.fromkeys(paired))


def initial_examples() -> list[int]:
    examples = []
    for row in range(58):
        assignment = sum(((column >> row) & 1) << wire
                         for wire, column in enumerate(Q5_INPUT_COLUMNS))
        expected = bool((Q5_TARGET >> row) & 1)
        if target(assignment) != expected:
            raise AssertionError((row, assignment, expected))
        examples.append(assignment)
    return paired_assignments(list(dict.fromkeys(examples)))


def load_examples(path: Path) -> list[int]:
    if not path.exists():
        return initial_examples()
    values = json.loads(path.read_text(encoding="utf-8"))
    examples = [int(value) for value in values]
    if any(value < 0 or value >= (1 << INPUTS) for value in examples):
        raise ValueError("example assignment outside the 14-input table")
    return paired_assignments(initial_examples() + examples)


def selected_value(
    clauses: list[list[int]],
    variables: Variables,
    example_index: int,
    assignment: int,
    selectors: list[int],
    selected: int,
) -> None:
    for wire, selector in enumerate(selectors):
        if wire < INPUTS:
            clauses.append([-selector, selected if (assignment >> wire) & 1 else -selected])
        else:
            source = variables.value[example_index][wire - INPUTS]
            clauses.append([-selector, -selected, source])
            clauses.append([-selector, selected, -source])


def build(
    examples: list[int],
    not_count: int | None = None,
    not_position: int | None = None,
) -> tuple[Variables, list[list[int]]]:
    variables = Variables(len(examples))
    clauses: list[list[int]] = []
    for gate in range(GATES):
        exactly_one(clauses, variables.op[gate])
        exactly_one(clauses, variables.left[gate])
        exactly_one(clauses, variables.right[gate])
        and_op, or_op, not_op = variables.op[gate]
        for left_wire, left_selector in enumerate(variables.left[gate]):
            for right_wire, right_selector in enumerate(variables.right[gate]):
                if left_wire > right_wire:
                    clauses.append([-and_op, -left_selector, -right_selector])
                    clauses.append([-or_op, -left_selector, -right_selector])
                if left_wire != right_wire:
                    clauses.append([-not_op, -left_selector, -right_selector])

    if not_position is not None:
        if not_position < 0 or not_position >= GATES:
            raise ValueError("NOT position outside the gate list")
        for gate in range(GATES):
            clauses.append([variables.op[gate][2] if gate == not_position
                            else -variables.op[gate][2]])
    elif not_count is not None:
        not_variables = [variables.op[gate][2] for gate in range(GATES)]
        if not_count == 0:
            clauses.extend([[-variable] for variable in not_variables])
        elif not_count == 1:
            exactly_one(clauses, not_variables)
        else:
            raise ValueError("only exact NOT counts zero and one are currently encoded")

    # A size-minimal solution is live.  This also permits a shorter solution to
    # be padded by a live idempotent gate, so it does not exclude size <= 26.
    for source_gate in range(GATES - 1):
        source_wire = INPUTS + source_gate
        uses = []
        for consumer in range(source_gate + 1, GATES):
            uses.append(variables.left[consumer][source_wire])
            uses.append(variables.right[consumer][source_wire])
        clauses.append(uses)

    for example_index, assignment in enumerate(examples):
        for gate in range(GATES):
            left = variables.left_value[example_index][gate]
            right = variables.right_value[example_index][gate]
            value = variables.value[example_index][gate]
            selected_value(clauses, variables, example_index, assignment,
                           variables.left[gate], left)
            selected_value(clauses, variables, example_index, assignment,
                           variables.right[gate], right)
            and_op, or_op, not_op = variables.op[gate]
            clauses.extend([
                [-and_op, -left, -right, value],
                [-and_op, left, -value],
                [-and_op, right, -value],
                [-or_op, left, right, -value],
                [-or_op, -left, value],
                [-or_op, -right, value],
                [-not_op, left, value],
                [-not_op, -left, -value],
            ])
        output = variables.value[example_index][GATES - 1]
        clauses.append([output if target(assignment) else -output])
    return variables, clauses


def encode(
    example_path: Path,
    cnf_path: Path,
    not_count: int | None = None,
    not_position: int | None = None,
) -> int:
    examples = load_examples(example_path)
    variables, clauses = build(examples, not_count=not_count,
                               not_position=not_position)
    with cnf_path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {variables.next_id - 1} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    print(json.dumps({
        "examples": len(examples),
        "variables": variables.next_id - 1,
        "clauses": len(clauses),
        "cnf": str(cnf_path),
        "not_count": not_count,
        "not_position": not_position,
        "paired_restriction_input": RESTRICTION_INPUT,
    }, sort_keys=True))
    return 0


def positive_model(path: Path) -> set[int] | None:
    text = path.read_text(encoding="ascii", errors="replace")
    if "s UNSATISFIABLE" in text:
        return None
    if "s SATISFIABLE" not in text:
        raise ValueError("solver output has no SAT verdict")
    return {
        int(token)
        for line in text.splitlines()
        if line.startswith("v ")
        for token in line[2:].split()
        if token != "0" and not token.startswith("-")
    }


def decode_model(model_path: Path, example_path: Path) -> list[list[int]] | None:
    positive = positive_model(model_path)
    if positive is None:
        print("UNSAT")
        return None
    variables = Variables(len(load_examples(example_path)))
    gates = []
    for gate in range(GATES):
        op = next(index for index, var in enumerate(variables.op[gate]) if var in positive)
        left = next(index for index, var in enumerate(variables.left[gate]) if var in positive)
        right = next(index for index, var in enumerate(variables.right[gate]) if var in positive)
        gates.append([op, left, right])
    return gates


def eval_gates(gates: list[list[int]], assignment: int) -> bool:
    wires = [bool((assignment >> wire) & 1) for wire in range(INPUTS)]
    for op, left, right in gates:
        if op == 0:
            wires.append(wires[left] and wires[right])
        elif op == 1:
            wires.append(wires[left] or wires[right])
        else:
            wires.append(not wires[left])
    return wires[-1]


def check(model_path: Path, example_path: Path, add_count: int) -> int:
    gates = decode_model(model_path, example_path)
    if gates is None:
        return 20
    false_positives = [assignment for assignment in range(1 << INPUTS)
                       if eval_gates(gates, assignment) and not target(assignment)]
    false_negatives = [assignment for assignment in range(1 << INPUTS)
                       if not eval_gates(gates, assignment) and target(assignment)]
    misses = false_positives + false_negatives
    record = {"gates": gates, "output": INPUTS + GATES - 1,
              "fitness": len(misses)}
    print(json.dumps(record, separators=(",", ":")))
    if not misses:
        print("WITNESS")
        return 0
    examples = load_examples(example_path)
    known = set(examples)
    def spread(values: list[int], count: int) -> list[int]:
        if count <= 0 or not values:
            return []
        if len(values) <= count:
            return values
        return [values[min(len(values) - 1, ((2 * index + 1) * len(values)) // (2 * count))]
                for index in range(count)]

    fresh_fp = [assignment for assignment in false_positives if assignment not in known]
    fresh_fn = [assignment for assignment in false_negatives if assignment not in known]
    half = max(1, add_count // 2)
    chosen = list(dict.fromkeys(spread(fresh_fp, half) + spread(fresh_fn, add_count - half)))
    if not chosen:
        chosen = spread([assignment for assignment in misses if assignment not in known], 1)
    chosen = [assignment for assignment in paired_assignments(chosen)
              if assignment not in known]
    example_path.write_text(json.dumps(examples + chosen, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    print(json.dumps({"misses": len(misses), "false_positives": len(false_positives),
                      "false_negatives": len(false_negatives), "added": len(chosen),
                      "examples": len(examples) + len(chosen)}, sort_keys=True))
    return 10


def main() -> int:
    if len(sys.argv) < 2:
        return 64
    command = sys.argv[1]
    if command == "init" and len(sys.argv) == 3:
        path = Path(sys.argv[2])
        path.write_text(json.dumps(initial_examples(), separators=(",", ":")) + "\n",
                        encoding="utf-8")
        print(len(initial_examples()))
        return 0
    if command == "encode" and len(sys.argv) in {4, 5, 6}:
        return encode(Path(sys.argv[2]), Path(sys.argv[3]),
                      int(sys.argv[4]) if len(sys.argv) >= 5 else None,
                      int(sys.argv[5]) if len(sys.argv) == 6 else None)
    if command == "check" and len(sys.argv) in {4, 5}:
        return check(Path(sys.argv[2]), Path(sys.argv[3]),
                     int(sys.argv[4]) if len(sys.argv) == 5 else 32)
    print(f"usage: {Path(sys.argv[0]).name} init EXAMPLES | "
          "encode EXAMPLES CNF [NOT_COUNT [NOT_POSITION]] | "
          "check MODEL EXAMPLES [ADD]", file=sys.stderr)
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
