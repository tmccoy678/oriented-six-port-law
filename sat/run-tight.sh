#!/usr/bin/env bash

set -euo pipefail

solver="${1:-cadical}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work="${TMPDIR:-/tmp}/oriented-six-port-law"
cnf="$work/L_meta_9753_three_star_tight.cnf"
solver_log="$work/three-star-tight.solver.log"
local_json="$work/three-star-tight.local.json"
full_witness="$work/L-meta-9753.witness.log"
expected=93259dc4c97f3291d8e59f94ddf759d7d5d8131d13517de002ecaf6c63beba6c

mkdir -p "$work"
python3 "$root/sat/synth_three_star_return_sat.py" encode-tight "$cnf"
actual="$(python3 -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "$cnf")"
if [[ "$actual" != "$expected" ]]; then
  printf 'CNF hash mismatch: expected %s, got %s\n' "$expected" "$actual" >&2
  exit 2
fi

set +e
"$solver" "$cnf" > "$solver_log" 2>&1
verdict=$?
set -e

case "$verdict" in
  10)
    python3 "$root/sat/synth_three_star_return_sat.py" decode "$solver_log" > "$local_json"
    python3 "$root/sat/assemble_three_star_L_meta_9753.py" "$local_json" > "$full_witness"
    printf 'SAT; full witness: %s\n' "$full_witness"
    ;;
  20)
    printf 'UNSAT for the frozen tight normal form; unrestricted status unchanged.\n'
    ;;
  *)
    printf 'CaDiCaL returned %s; log: %s\n' "$verdict" "$solver_log" >&2
    exit "$verdict"
    ;;
esac
