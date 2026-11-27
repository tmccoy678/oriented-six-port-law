import PEqualNP.MetaComplexity.Helpers.PermInputs

/-!
# Zero-factorial cyclic symmetry reduction

The isolated three-star target has a threefold input symmetry. Every decoded
witness has a first gate and at least one selected input. Rotating the complete
witness can move that input into the representative set `{0, 3, 6}` without
changing the function or gate count.
-/

namespace PEqualNP.ZeroFactorialSymmetry

open PEqualNP.CircuitLowerBounds PEqualNP.MetaComplexity
open PEqualNP.MetaComplexity.Helpers.PermInputs

def routeNext (index : Fin 9) : Fin 9 :=
  match index.val with
  | 0 => 2
  | 1 => 0
  | 2 => 1
  | 3 => 4
  | 4 => 5
  | 5 => 3
  | 6 => 8
  | 7 => 6
  | _ => 7

def routeCycle : Equiv.Perm (Fin 9) where
  toFun := routeNext
  invFun := fun index => routeNext (routeNext index)
  left_inv := by intro index; fin_cases index <;> rfl
  right_inv := by intro index; fin_cases index <;> rfl

theorem route_return (index : Fin 9) :
    routeCycle (routeCycle (routeCycle index)) = index := by
  fin_cases index <;> rfl

def target (x : Fin 9 → Bool) : Bool :=
  (x 0 && (x 3 || x 4 || x 6)) ||
  (x 1 && (x 3 || x 5 || x 7)) ||
  (x 2 && (x 4 || x 5 || x 8))

theorem target_route_invariant :
    ∀ x : Fin 9 → Bool, target (x ∘ routeCycle) = target x := by
  native_decide

def Representative (index : Fin 9) : Prop :=
  index = 0 ∨ index = 3 ∨ index = 6

theorem representative_or_rotated (index : Fin 9) :
    Representative index ∨
    Representative (routeCycle index) ∨
    Representative (routeCycle (routeCycle index)) := by
  fin_cases index <;> simp [Representative, routeCycle, routeNext]

structure SearchWitness (bound : Nat) where
  circuit : Circuit
  fanInTwo : FanInTwo circuit
  size : circuit.size ≤ bound
  computes : ∀ x : Fin 9 → Bool, circuit.eval (List.ofFn x) = target x
  distinguished : Fin 9
  distinguished_spec : ∃ gate, circuit.gates.head? = some gate ∧
    (distinguished : Nat) ∈ gate.inputs

def rotateWitness {bound : Nat} (witness : SearchWitness bound) : SearchWitness bound where
  circuit := relabel 9 9 routeCycle witness.circuit
  fanInTwo := by
    intro gate hgate
    obtain ⟨source, hsource, rfl⟩ := List.mem_map.1 hgate
    exact ⟨(witness.fanInTwo source hsource).1,
      by simpa [relGate] using (witness.fanInTwo source hsource).2⟩
  size := by simpa [relabel, Circuit.size] using witness.size
  computes := by
    intro x
    calc
      (relabel 9 9 routeCycle witness.circuit).eval (List.ofFn x) =
          witness.circuit.eval (List.ofFn (x ∘ routeCycle)) := by
            have hrel := (rel_fold 9 9 routeCycle witness.circuit.gates _ _
              (rel_init 9 9 routeCycle x)).2.2 witness.circuit.output
            change
              (List.foldl PEqualNP.MetaComplexity.Helpers.PermInputs.step
                  (List.ofFn x)
                  (witness.circuit.gates.map (relGate 9 9 routeCycle))).getD
                    (wmap 9 9 routeCycle witness.circuit.output) false =
              (List.foldl PEqualNP.MetaComplexity.Helpers.PermInputs.step
                  (List.ofFn (x ∘ routeCycle)) witness.circuit.gates).getD
                    witness.circuit.output false
            exact hrel
      _ = target (x ∘ routeCycle) := witness.computes _
      _ = target x := target_route_invariant x
  distinguished := routeCycle witness.distinguished
  distinguished_spec := by
    obtain ⟨gate, hgate, hinput⟩ := witness.distinguished_spec
    refine ⟨relGate 9 9 routeCycle gate, ?_, ?_⟩
    · simp [relabel, hgate]
    · have hm : wmap 9 9 routeCycle (witness.distinguished : Nat) ∈
          gate.inputs.map (wmap 9 9 routeCycle) :=
        List.mem_map.2 ⟨_, hinput, rfl⟩
      simpa [relGate, wmap] using hm

theorem every_witness_has_representative {bound : Nat}
    (witness : SearchWitness bound) :
    ∃ canonical : SearchWitness bound, Representative canonical.distinguished := by
  rcases representative_or_rotated witness.distinguished with h | h | h
  · exact ⟨witness, h⟩
  · exact ⟨rotateWitness witness, h⟩
  · exact ⟨rotateWitness (rotateWitness witness), h⟩

end PEqualNP.ZeroFactorialSymmetry
