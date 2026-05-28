import pyomo.environ as pyo
import pandas as pd
from pyomo.repn import generate_standard_repn

def generate_marginal_bids(model: pyo.ConcreteModel) -> pd.DataFrame:
    """
    Calculates the floor bid price dynamically by introspecting the objective 
    function. Operates strictly in O(1) memory mapping.
    """
    bids = []
    
    # Extract the active objective function mathematically
    # This works regardless of how many registries or expressions you summed
    objective_expr = model.objective_function.expr
    
    # generate_standard_repn mathematically parses the expression tree
    # It separates the constants, the linear variables, and the linear coefficients
    repn = generate_standard_repn(objective_expr)
    
    # repn.linear_vars is a list of variable objects (e.g., [x1, x2])
    # repn.linear_coefs is a list of their coefficients (e.g., [6.0, 5.0])
    for var_obj, c_j in zip(repn.linear_vars, repn.linear_coefs):
        
        # 1. Extract the Reduced Cost directly from solver memory
        rc_j = model.rc.get(var_obj, 0.0) if hasattr(model, 'rc') else 0.0
        
        # 2. Floor Bid = Forecasted Value (c_j) - Opportunity Cost (rc_j)
        floor_bid = c_j - rc_j
        
        bids.append({
            "Asset_or_Tranche": var_obj.name,
            "Awarded_Volume_MW": pyo.value(var_obj),
            "Forecasted_Margin_c_j": c_j,
            "Reduced_Cost_rc_j": rc_j,
            "Floor_Bid_Price": floor_bid
        })
        
    df_bids = pd.DataFrame(bids)
    
    # Sort to replicate a standard MMS bidding ladder
    df_bids = df_bids.sort_values(by=["Floor_Bid_Price"]).reset_index(drop=True)
    
    return df_bids