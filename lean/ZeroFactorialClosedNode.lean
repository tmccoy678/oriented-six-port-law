import Mathlib.Data.Nat.Factorial.Basic

/-!
# Closed three-family node

The nine minimal positive supports of the isolated three-star target form a
closed adjacent route. Its three family junctions are 4, 5 and 3; reversing
the route gives the opposite orientation. The family rotation and mirror
satisfy the dihedral return law.
-/

namespace PEqualNP.ZeroFactorialClosedNode

structure Edge where
  left : Fin 9
  right : Fin 9
  deriving DecidableEq, Repr

def landmarks : List Edge :=
  [⟨0, 3⟩, ⟨0, 4⟩, ⟨0, 6⟩,
   ⟨1, 3⟩, ⟨1, 5⟩, ⟨1, 7⟩,
   ⟨2, 4⟩, ⟨2, 5⟩, ⟨2, 8⟩]

def route : List Edge :=
  [⟨0, 3⟩, ⟨0, 6⟩, ⟨0, 4⟩,
   ⟨2, 4⟩, ⟨2, 8⟩, ⟨2, 5⟩,
   ⟨1, 5⟩, ⟨1, 7⟩, ⟨1, 3⟩]

def mirrorRoute : List Edge :=
  [⟨0, 3⟩, ⟨1, 3⟩, ⟨1, 7⟩,
   ⟨1, 5⟩, ⟨2, 5⟩, ⟨2, 8⟩,
   ⟨2, 4⟩, ⟨0, 4⟩, ⟨0, 6⟩]

def sharesVertex (first second : Edge) : Bool :=
  decide (first.left = second.left ∨ first.left = second.right ∨
    first.right = second.left ∨ first.right = second.right)

def chainFrom (previous : Edge) : List Edge → Bool
  | [] => true
  | current :: rest => sharesVertex previous current && chainFrom current rest

def closedChain : List Edge → Bool
  | [] => false
  | first :: rest => chainFrom first rest &&
      match (first :: rest).getLast? with
      | none => false
      | some last => sharesVertex last first

def sharedVertex (first second : Edge) : Option (Fin 9) :=
  if first.left = second.left ∨ first.left = second.right then some first.left
  else if first.right = second.left ∨ first.right = second.right then some first.right
  else none

theorem zero_factorial_identity : Nat.factorial 0 = 1 := by
  rfl

theorem route_exact_cover : route.Perm landmarks := by
  native_decide

theorem route_nodup : route.Nodup := by
  native_decide

theorem route_closed : closedChain route = true := by
  native_decide

theorem mirror_exact_cover : mirrorRoute.Perm landmarks := by
  native_decide

theorem mirror_closed : closedChain mirrorRoute = true := by
  native_decide

theorem three_junctions :
    sharedVertex ⟨0, 4⟩ ⟨2, 4⟩ = some 4 ∧
    sharedVertex ⟨2, 5⟩ ⟨1, 5⟩ = some 5 ∧
    sharedVertex ⟨1, 3⟩ ⟨0, 3⟩ = some 3 := by
  native_decide

inductive Family where
  | family0
  | family2
  | family1
  deriving DecidableEq, Repr

def rotate : Family → Family
  | .family0 => .family2
  | .family2 => .family1
  | .family1 => .family0

def mirror : Family → Family
  | .family0 => .family0
  | .family2 => .family1
  | .family1 => .family2

def rotateInv (family : Family) : Family := rotate (rotate family)

theorem rotate_three_return (family : Family) :
    rotate (rotate (rotate family)) = family := by
  cases family <;> rfl

theorem mirror_two_return (family : Family) :
    mirror (mirror family) = family := by
  cases family <;> rfl

theorem mirror_rotate_mirror (family : Family) :
    mirror (rotate (mirror family)) = rotateInv family := by
  cases family <;> rfl

def orientedNodes : List (Family × Bool) :=
  [(.family0, false), (.family0, true),
   (.family2, false), (.family2, true),
   (.family1, false), (.family1, true)]

theorem oriented_node_count : orientedNodes.length = 6 := by
  rfl

end PEqualNP.ZeroFactorialClosedNode
