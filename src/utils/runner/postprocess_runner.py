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
    export_audit_files(model, output_dir="audit_data")
    logger.info("STEP 6.1 SUCCESS: Primal and Dual Files Exported Successfully")
    
    logger.info("STEP 6.2 ATTEMPT: Calculating and Exporting Marginal Floor Bids.")
    bid_ladder = generate_marginal_bids(model)
    
    auctionbids_dir = "auctionbids"
    os.makedirs(auctionbids_dir, exist_ok=True)
    bid_csv_path = os.path.join(auctionbids_dir, f"{model.name}_marginal_bids.csv")
    bid_ladder.to_csv(bid_csv_path, index=False)
    logger.info(f"STEP 6.2 SUCCESS: Bids saved to {bid_csv_path}")
    
    logger.info("STEP 6.3 ATTEMPT: Logging Generated Bid Ladder.")
    logger.info("STEP 6.3 SUCCESS: Generated Bid Ladder Logged Successfully")
    logger.info("STEP 6 SUCCESS: Results Extracted and Logged Successfully")
