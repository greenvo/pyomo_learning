import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.utils.logger_factory import setup_logger
from src.utils.factory.solver_factory import pyomo_solver_creator
from src.builder.polytope import build_model
from src.builder.orchestrator import orchestrate_model
from src.utils.runner.solution_extractor import add_solution_extraction

logger = setup_logger(__name__, "solver.log")

def run_solver():
    logger.info("STEP 1 ATTEMPT: Building Polytope")
    stage1_model = build_model()
    
    if stage1_model is None:
        logger.error("Model was not built.")
        return None
    else:        
        logger.info("STEP 1 SUCCESS: Model built successfully.")

    logger.info("STEP 2 ATTEMPT: Orchestrating Model (Dynamically resolving Variables, Objectives, Constraints)")
    orchestrate_model(stage1_model)
    logger.info("STEP 2 SUCCESS: Model Orchestrated Successfully")
    
    logger.info("STEP 3 ATTEMPT: Adding Solution Extraction.")
    add_solution_extraction(stage1_model)
    logger.info("STEP 3 SUCCESS: Solution Extraction Added Successfully")
    
    logger.info("STEP 4 ATTEMPT: Creating Solver.")
    solver = pyomo_solver_creator(solver_name='appsi_highs')
    logger.info("STEP 4 SUCCESS: Solver Created Successfully")
    
    logger.info("STEP 5 ATTEMPT: Solving Model.")
    results = solver.solve(stage1_model, tee=True) 
    logger.info("STEP 5 SUCCESS: Model Solved")
    
    return stage1_model
