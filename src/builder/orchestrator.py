from src.datastore.coeff import STAGE
from src.builder.variable_builder import build_variables
from src.builder.objective_builder import build_objectives
from src.builder.constraint_builder import build_constraints
from src.utils.logger_factory import setup_logger

logger = setup_logger(__name__, "orchestrator.log")

def orchestrate_model(model):
    if STAGE != 1:
        logger.warning(f"Orchestrator called for STAGE {STAGE}, but currently only supports STAGE 1.")
        return

    logger.info("Starting model orchestration...")
    
    build_variables(model)
    build_objectives(model)
    build_constraints(model)
    
    logger.info("Model orchestration complete.")
