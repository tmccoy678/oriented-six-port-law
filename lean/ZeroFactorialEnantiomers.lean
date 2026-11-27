import ZeroFactorialSymmetry

/-!
# Mirror-paired zero-factorial representatives

The first cyclic slice chooses `{0, 3, 6}`. Its exact mirror is `{0, 4, 6}`.
Both slices contain a rotated representative of every decoded witness.
-/

namespace PEqualNP.ZeroFactorialEnantiomers

open PEqualNP.ZeroFactorialSymmetry

def LeftRepresentative (index : Fin 9) : Prop :=
  index = 0 ∨ index = 4 ∨ index = 6

def inputMirror (index : Fin 9) : Fin 9 :=
  match index.val with
  | 0 => 0
  | 1 => 2
  | 2 => 1
  | 3 => 4
  | 4 => 3
  | 5 => 5
  | 6 => 6
  | 7 => 8
  | _ => 7

theorem input_mirror_involution (index : Fin 9) :
    inputMirror (inputMirror index) = index := by
  fin_cases index <;> rfl

theorem mirror_maps_right_to_left (index : Fin 9)
    (h : Representative index) : LeftRepresentative (inputMirror index) := by
  fin_cases index <;> simp_all [Representative, LeftRepresentative, inputMirror]

theorem left_representative_or_rotated (index : Fin 9) :
    LeftRepresentative index ∨
    LeftRepresentative (routeCycle index) ∨
    LeftRepresentative (routeCycle (routeCycle index)) := by
  fin_cases index <;> simp [LeftRepresentative, routeCycle, routeNext]

theorem every_witness_has_left_representative {bound : Nat}
    (witness : SearchWitness bound) :
    ∃ canonical : SearchWitness bound,
      LeftRepresentative canonical.distinguished := by
  rcases left_representative_or_rotated witness.distinguished with h | h | h
  · exact ⟨witness, h⟩
  · exact ⟨rotateWitness witness, h⟩
  · exact ⟨rotateWitness (rotateWitness witness), h⟩

end PEqualNP.ZeroFactorialEnantiomers
