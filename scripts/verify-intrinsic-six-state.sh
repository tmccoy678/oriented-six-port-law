#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
pnp_root="${1:?usage: verify-intrinsic-six-state.sh /path/to/pequalnp-proofs}"
expected="fff8fe2fb81a0184a99b80348810e1d8147ff2c2"

test "$(git -C "$pnp_root" rev-parse HEAD)" = "$expected" || {
  echo "refused: pequalnp-proofs must be pinned to $expected" >&2
  exit 2
}

cd "$pnp_root/lean"
lake build PEqualNP.MetaComplexity.Helpers.PermInputs

lake env lean -R "$repo_root/lean" \
  -o .lake/build/lib/lean/ZeroFactorialNodeSearch.olean \
  "$repo_root/lean/ZeroFactorialNodeSearch.lean"
lake env lean -R "$repo_root/lean" \
  -o .lake/build/lib/lean/ZeroFactorialSymmetry.olean \
  "$repo_root/lean/ZeroFactorialSymmetry.lean"
lake env lean -R "$repo_root/lean" \
  -o .lake/build/lib/lean/ZeroFactorialEnantiomers.olean \
  "$repo_root/lean/ZeroFactorialEnantiomers.lean"
lake env lean -R "$repo_root/lean" \
  -o .lake/build/lib/lean/ZeroFactorialClosedNode.olean \
  "$repo_root/lean/ZeroFactorialClosedNode.lean"
lake env lean -R "$repo_root/lean" \
  "$repo_root/lean/IntrinsicSixStateChild.lean"

echo "intrinsic six-state Lean verification: ACCEPT"
