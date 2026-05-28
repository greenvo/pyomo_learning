import pyomo.environ as pyo
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.utils.factory.solver_factory import pyomo_solver_creator
from src.builder.polytope import build_model
from src.builder.orchestrator import orchestrate_model
from src.utils.runner.solution_extractor import add_solution_extraction

def main():
    print("Building Polytope...")
    stage1_model = build_model()
    
    if stage1_model is None:
        print("Model was not built.")
        return

    print("Orchestrating Model (Dynamically resolving Variables, Objectives, Constraints)...")
    orchestrate_model(stage1_model)
    
    print("Adding Solution Extraction...")
    add_solution_extraction(stage1_model)
    
    print("Creating Solver...")
    solver = pyomo_solver_creator(solver_name='appsi_highs')
    
    print("Solving Model...")
    results = solver.solve(stage1_model, tee=True)
    
    print("\n--- Final Results ---")
    print(f"x1 = {pyo.value(stage1_model.x1)}")
    print(f"x2 = {pyo.value(stage1_model.x2)}")
    print(f"Objective = {pyo.value(stage1_model.objective_function)}")
    
    if hasattr(stage1_model, "add_c1_stage1_constraint"):
        print(f"Dual for c1 (pi 1) = {stage1_model.dual[stage1_model.add_c1_stage1_constraint]}")
    if hasattr(stage1_model, "add_c2_stage1_constraint"):
        print(f"Dual for c2 (pi 2) = {stage1_model.dual[stage1_model.add_c2_stage1_constraint]}")

if __name__ == "__main__":
    main()
