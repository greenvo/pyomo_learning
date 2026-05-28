import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.utils.logger_factory import setup_logger
from src.utils.runner.solve_runner import run_solver
from src.utils.runner.postprocess_runner import run_postprocessing

logger = setup_logger(__name__, "main.log")

def main():
    logger.info("Starting Execution Pipeline")
    
    # Run the solver pipeline
    model = run_solver()
    
    if model is not None:
        # Run the post-processing pipeline
        run_postprocessing(model)
        
    logger.info("Execution Pipeline Complete")

if __name__ == "__main__":
    main()
