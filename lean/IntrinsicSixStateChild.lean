import ZeroFactorialEnantiomers
import ZeroFactorialClosedNode
import ZeroFactorialNodeSearch

/-!
# Intrinsic six-state search body

One finite search body carries three family phases and both handed
orientations. Each bounded subquestion carries the exact cost of its established
checker.
-/

namespace PEqualNP.IntrinsicSixStateChild

inductive Hand where
  | right
  | left
  deriving DecidableEq, Repr

def flip : Hand → Hand
  | .right => .left
  | .left => .right

structure State where
  family : PEqualNP.ZeroFactorialClosedNode.Family
  hand : Hand
  deriving DecidableEq, Repr

def turn (state : State) : State :=
  ⟨PEqualNP.ZeroFactorialClosedNode.rotate state.family, state.hand⟩

def reflect (state : State) : State :=
  ⟨PEqualNP.ZeroFactorialClosedNode.mirror state.family, flip state.hand⟩

theorem turn_three_return (state : State) :
    turn (turn (turn state)) = state := by
  rcases state with ⟨family, hand⟩
  cases family <;> cases hand <;> rfl

theorem reflect_two_return (state : State) :
    reflect (reflect state) = state := by
  rcases state with ⟨family, hand⟩
  cases family <;> cases hand <;> rfl

def turnInv (state : State) : State := turn (turn state)

theorem reflect_turn_reflect (state : State) :
    reflect (turn (reflect state)) = turnInv state := by
  rcases state with ⟨family, hand⟩
  cases family <;> cases hand <;> rfl

def allStates : List State :=
  [⟨.family0, .right⟩, ⟨.family0, .left⟩,
   ⟨.family2, .right⟩, ⟨.family2, .left⟩,
   ⟨.family1, .right⟩, ⟨.family1, .left⟩]

theorem six_state_count : allStates.length = 6 := by
  rfl

theorem every_witness_has_both_hands {bound : Nat}
    (witness : PEqualNP.ZeroFactorialSymmetry.SearchWitness bound) :
    ∃ right left : PEqualNP.ZeroFactorialSymmetry.SearchWitness bound,
      PEqualNP.ZeroFactorialSymmetry.Representative right.distinguished ∧
      PEqualNP.ZeroFactorialEnantiomers.LeftRepresentative left.distinguished := by
  obtain ⟨right, hright⟩ :=
    PEqualNP.ZeroFactorialSymmetry.every_witness_has_representative witness
  obtain ⟨left, hleft⟩ :=
    PEqualNP.ZeroFactorialEnantiomers.every_witness_has_left_representative witness
  exact ⟨right, left, hright, hleft⟩

inductive QuestionKind where
  | nodeRoute
  | orientation
  | localWitness
  | fullWitness
  deriving DecidableEq, Repr

structure CheckContract where
  kind : QuestionKind
  structuralRank : Nat
  verificationSteps : Nat
  deriving DecidableEq, Repr

def nodeContract : CheckContract :=
  ⟨.nodeRoute, 9, 9⟩

def orientationContract : CheckContract :=
  ⟨.orientation, 3, 3⟩

def localWitnessContract : CheckContract :=
  ⟨.localWitness, 0, 2 ^ 9 * 10⟩

def fullWitnessContract : CheckContract :=
  ⟨.fullWitness, 0, 2 ^ 14 * 26⟩

theorem intrinsic_costs :
    nodeContract.structuralRank = 9 ∧
    orientationContract.structuralRank = 3 ∧
    localWitnessContract.verificationSteps = 5120 ∧
    fullWitnessContract.verificationSteps = 425984 := by
  decide

theorem zero_factorial_carrier : Nat.factorial 0 = 1 := by
  rfl

end PEqualNP.IntrinsicSixStateChild
