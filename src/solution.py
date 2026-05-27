import pyomo.environ as pyo
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.create_solver import pyomo_solver_creator

from src.polytope_building import build_model
from src.variable_store import add_variables
from src.objective_store import store_objectives
from src.orchestration import orchestrate_model
from src.solution_extraction import add_solution_extraction

def main():
    print("Building Polytope...")
    stage_1_model = build_model()
    
    if stage_1_model is None:
        print("Model was not built.")
        return

    print("Adding Variables...")
    add_variables(stage_1_model)
    
    print("Storing Objectives Expressions...")
    store_objectives(stage_1_model)
    
    print("Orchestrating Model (Building Constraints & Objectives dynamically)...")
    orchestrate_model(stage_1_model)
    
    print("Adding Solution Extraction...")
    add_solution_extraction(stage_1_model)
    
    print("Creating Solver...")
    solver = pyomo_solver_creator(solver_name='appsi_highs')
    
    print("Solving Model...")
    results = solver.solve(stage_1_model, tee=True)
    
    print("\n--- Final Results ---")
    print(f"x1 = {pyo.value(stage_1_model.x1)}")
    print(f"x2 = {pyo.value(stage_1_model.x2)}")
    print(f"Objective = {pyo.value(stage_1_model.objective_function)}")
    
    if hasattr(stage_1_model, "add_c1__stage_1_constraint"):
        print(f"Dual for c1 (pi 1) = {stage_1_model.dual[stage_1_model.add_c1__stage_1_constraint]}")
    if hasattr(stage_1_model, "add_c2_stage_1_constraint"):
        print(f"Dual for c2 (pi 2) = {stage_1_model.dual[stage_1_model.add_c2_stage_1_constraint]}")

if __name__ == "__main__":
    main()
