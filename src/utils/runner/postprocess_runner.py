import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(PROJECT_ROOT)

from src.utils.logger_factory import setup_logger
from src.utils.runner.auditor import export_audit_files
from src.postprocess.bidgenerator import generate_marginal_bids

logger = setup_logger(__name__, "postprocess.log")

def run_postprocessing(model):
    if model is None:
        logger.error("No model provided for post-processing.")
        return
        
    logger.info("STEP 6 ATTEMPT: Extracting and Logging Results.")

    logger.info("STEP 6.1 ATTEMPT: Exporting Primal and Dual Files.")
    export_audit_files(model, output_dir="auctionbids")
    logger.info("STEP 6.1 SUCCESS: Primal and Dual Files Exported Successfully")
    
    logger.info("STEP 6.2 ATTEMPT: Calculating Marginal Floor Bids.")
    bid_ladder = generate_marginal_bids(model)
    logger.info("STEP 6.2 SUCCESS: Marginal Floor Bids Calculated Successfully")
    
    logger.info("STEP 6.3 ATTEMPT: Logging Generated Bid Ladder.")
    logger.info("\n--- GENERATED BID LADDER ---")
    logger.info(f"\n{bid_ladder.to_string(index=False)}")
    logger.info("STEP 6.3 SUCCESS: Generated Bid Ladder Logged Successfully")
    logger.info("STEP 6 SUCCESS: Results Extracted and Logged Successfully")
