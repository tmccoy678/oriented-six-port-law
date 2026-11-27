import Mathlib.Data.Nat.Factorial.Basic

/-!
# Zero-factorial node search

A finite search scaffold for the isolated nine-input, ten-gate three-star
return cell. The search inherits `0! = 1` as an uncounted carrier, begins with
no covered prime implicants, advances through three balanced node phases, and
accepts only an exact adjacent route through all nine landmarks.
-/

namespace PEqualNP.ZeroFactorialNodeSearch

inductive Phase where
  | northSouth
  | eastWest
  | depthPair
  deriving DecidableEq, Repr

def Phase.next : Phase → Phase
  | .northSouth => .eastWest
  | .eastWest => .depthPair
  | .depthPair => .northSouth

theorem Phase.return_after_three (phase : Phase) :
    phase.next.next.next = phase := by
  cases phase <;> rfl

inductive Node where
  | empty
  | pair (phase : Phase)
  | saturated
  deriving DecidableEq, Repr

def interact : Node → Node
  | .empty => .empty
  | .pair phase => .pair phase.next
  | .saturated => .empty

theorem pair_return (phase : Phase) :
    interact (interact (interact (.pair phase))) = .pair phase := by
  cases phase <;> rfl

theorem saturated_shock_to_empty : interact .saturated = .empty := by
  rfl

theorem zero_factorial_carrier : Nat.factorial 0 = 1 := by
  rfl

structure Edge where
  left : Fin 9
  right : Fin 9
  deriving DecidableEq, BEq, Repr

def landmarks : List Edge :=
  [⟨0, 3⟩, ⟨0, 4⟩, ⟨0, 6⟩,
   ⟨1, 3⟩, ⟨1, 5⟩, ⟨1, 7⟩,
   ⟨2, 4⟩, ⟨2, 5⟩, ⟨2, 8⟩]

def target (x : Fin 9 → Bool) : Bool :=
  (x 0 && (x 3 || x 4 || x 6)) ||
  (x 1 && (x 3 || x 5 || x 7)) ||
  (x 2 && (x 4 || x 5 || x 8))

def edgeInput (edge : Edge) : Fin 9 → Bool :=
  fun index => decide (index = edge.left ∨ index = edge.right)

def singletonInput (vertex : Fin 9) : Fin 9 → Bool :=
  fun index => decide (index = vertex)

def minimalPositive (edge : Edge) : Bool :=
  target (edgeInput edge) &&
  !(target (singletonInput edge.left)) &&
  !(target (singletonInput edge.right))

theorem landmarks_are_minimal_positive :
    landmarks.all minimalPositive = true := by
  native_decide

def sharesVertex (first second : Edge) : Bool :=
  decide (first.left = second.left ∨ first.left = second.right ∨
    first.right = second.left ∨ first.right = second.right)

def chainFrom (previous : Edge) : List Edge → Bool
  | [] => true
  | current :: rest => sharesVertex previous current && chainFrom current rest

def isChain : List Edge → Bool
  | [] => true
  | first :: rest => chainFrom first rest

def route : List Edge :=
  [⟨0, 3⟩, ⟨0, 6⟩, ⟨0, 4⟩,
   ⟨2, 4⟩, ⟨2, 8⟩, ⟨2, 5⟩,
   ⟨1, 5⟩, ⟨1, 3⟩, ⟨1, 7⟩]

structure SearchState where
  carrier : Nat
  phase : Phase
  covered : List Edge
  deriving DecidableEq, Repr

def seed : SearchState :=
  ⟨Nat.factorial 0, .northSouth, []⟩

def visit (state : SearchState) (edge : Edge) : SearchState :=
  { carrier := state.carrier
    phase := state.phase.next
    covered := state.covered ++ [edge] }

def runRoute (candidate : List Edge) : SearchState :=
  candidate.foldl visit seed

theorem route_preserves_carrier : (runRoute route).carrier = 1 := by
  native_decide

theorem route_returns_phase : (runRoute route).phase = .northSouth := by
  native_decide

theorem route_covers_exactly : (runRoute route).covered.Perm landmarks := by
  native_decide

theorem route_is_adjacent : isChain route = true := by
  native_decide

def verified : Bool :=
  isChain route &&
  (route.length == landmarks.length) &&
  decide route.Nodup &&
  route.all (fun edge => landmarks.contains edge) &&
  landmarks.all minimalPositive &&
  decide ((runRoute route).carrier = 1) &&
  decide ((runRoute route).phase = .northSouth) &&
  decide (interact .saturated = .empty)

theorem verified_true : verified = true := by
  native_decide

end PEqualNP.ZeroFactorialNodeSearch
