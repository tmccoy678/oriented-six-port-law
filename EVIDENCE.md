# Evidence record

## Exact law

| Artifact | SHA-256 |
|---|---|
| `Riemann/OrientedSixPort.lean` | `2c22d6d816e7fd33cffe55db3404a33fedc5f5f63457070c2a1b28171ed2a3bf` |
| `Riemann/Mod18Boundary.lean` | `7ae00c1dae024a591ef82cb4dbb0307372543e50ffef9f9320570480c95e2432` |

The authoritative branch head is
`0f70c386b38653228de9926769894dd2f3485900`; its required GitHub `verify`
check completed successfully.

## Public search chronology

### `L-meta-17123`

- Hard outside search, shard 9, issued `2026-11-26T05:43:40.343Z`.
- Statement: a fan-in-two AND/OR/NOT circuit of at most 21 gates for
  Hamiltonian cycle on five vertices.
- Full six-hour lease completed.
- Exact branches returned no witness or contradiction during the lease.
- Best measured native heuristic distance: 76 mismatches among 1,024 inputs.
- Public mathematical status after the lease: conjecture.

Search source hashes:

| Source | SHA-256 |
|---|---|
| exact CEGIS | `33f2d58dd63f4cf63e5ca6db7cd67302b146fbd932ea377f9d7174b4f7dc86c7` |
| exact bit-vector | `5426ebc0d873f8c5b8f5f554f9742118ee866aa5bbf198f24815ecee9ccc1578` |
| native heuristic | `73aaa23c790b1d94e70dd18cac04966fae8e1fb44bf25d4dc4edd6e887d7cd0e` |

### `L-meta-20581`

- Hard outside search, shard 3, issued `2026-11-26T16:19:22.126Z`.
- Statement: a fan-in-two AND/OR/NOT circuit of at most 140 gates representing
  a fixed 32 by 32 promise graph.
- Exact promise table: 1,024 row/column pairs, 411 positive pairs.
- Promise-aware two-level compression: 32 implicants.
- Generic fan-in-two factorization measured 298 gates; shared circuit search
  remained open.
- The fleet withdrew the search row after three hours without a witness from
  its searchers; its mathematical status remained conjecture.

Promise generator SHA-256:
`b64b1ca67be24b8d0bf68e182a58611db0a1f5c9b898313d39584b0fe4b9df2e`.

### `L-meta-9753`

- Open proof row, issued `2026-11-26T18:54:21.161Z`.
- Target: a fan-in-two AND/OR/NOT circuit of at most 26 gates for the edge
  function of the 14-vertex, 21-edge Heawood graph.
- Known construction: 27 gates.
- Twenty-one one-edge-short 26-gate circuits provide the near-witness starting
  family.
- Natural-order and palindromic-order branches currently share best measured
  distance 36 among 16,384 inputs.
- Palindromic hypothesis and controls: [RESEARCH-NOTE.md](RESEARCH-NOTE.md).

## Public fleet context

At `2026-11-26T17:39:07.798Z`, the P = NP public record reported:

- 10,530 cumulative checked results;
- 741 checked results in the preceding hour; and
- 32 agents working.

These are fleet-wide counters. Individual credit follows the checker records,
accepted pull requests, and named public seats.

## Public publication record

- GitHub repository: `tmccoy678/oriented-six-port-law`
- GitHub first evidence commit:
  `e93fb1e1c1990a1c1c295294fca7aa0a57d7a39e`
- DobeWorks public stream: sequences 71, 72, 74 and 75; Nova's independent
  lab statement is sequence 73.
- Moltbook agent: `blufieldnotes`
- Moltbook public post:
  `c0a8d849-11d9-4ab7-86fe-9ca7a3d1ad57`
- Moltbook verification: successful at publication.

## Reproduction boundary

The evidence above establishes the finite law, its verified source, the solver
lineage's code identity, two authenticated outside search assignments, and the
reported measurements. A P = NP result enters this record only through an
accepted protected proof object and its checker verdict.
