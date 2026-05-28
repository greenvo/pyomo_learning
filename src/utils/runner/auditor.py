import os
import pandas as pd
import pyomo.environ as pyo

from src.datastore.LP_constants import TOLERANCE


def _derive_variable_basis(primal: float, rc: float) -> str:
    """Mathematically infers column basis status."""
    if abs(primal) > TOLERANCE:
        return "Basic"
    elif abs(rc) > TOLERANCE:
        return "Non-Basic at Bound"
    return "Degenerate (Basic at Bound)"

def _derive_constraint_basis(slack: float, pi: float) -> str:
    """Mathematically infers row basis status."""
    if abs(slack) > TOLERANCE:
        return "Basic (Slack Variable in Basis)"
    elif abs(pi) > TOLERANCE:
        return "Non-Basic (Constraint is Binding)"
    return "Degenerate (Binding with zero marginal value)"

def export_audit_files(model: pyo.ConcreteModel, output_dir: str = "auctionbids"):
    """
    Universally extracts primals, slacks, duals, and basis statuses for ANY model, 
    irrespective of the variable or constraint names.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # TASK 1: Abstract Extraction of Primals, RC, and Basis
    var_data = []
    # Natively loops through EVERY variable attached to the model
    for var_component in model.component_objects(pyo.Var, active=True):
        for index in var_component:
            var_obj = var_component[index]
            
            primal_val = pyo.value(var_obj)
            rc_val = model.rc.get(var_obj, 0.0) if hasattr(model, 'rc') else 0.0
            basis_status = _derive_variable_basis(primal_val, rc_val)
            
            var_data.append({
                "Decision Variable Name": var_obj.name,
                "Decision Variable Value": primal_val,
                "cj-zj (dual slack)": rc_val,
                "Basis": basis_status
            })
            
    df_vars = pd.DataFrame(var_data)
    df_vars.to_csv(os.path.join(output_dir, f"{model.name}_decision_variables_primals.csv"), index=False)

    # TASK 2: Abstract Extraction of Constraints, Slacks, Pi, and Basis
    constraint_data = []
    # Natively loops through EVERY constraint attached to the model
    for constr_component in model.component_objects(pyo.Constraint, active=True):
        for index in constr_component:
            constr_obj = constr_component[index]
            
            try:
                slack_val = float(constr_obj.slack())
            except (ValueError, TypeError):
                slack_val = 0.0
                
            pi_val = model.dual.get(constr_obj, 0.0) if hasattr(model, 'dual') else 0.0
            
            # Filter float noise
            if abs(slack_val) >= TOLERANCE:
                pi_val = 0.0  
                
            basis_status = _derive_constraint_basis(slack_val, pi_val)
            
            constraint_data.append({
                "Constraint Name": constr_obj.name,
                "Constraint Slack": slack_val,
                "Pi (marginal price)": pi_val,
                "Basis": basis_status
            })
            
    df_constraints = pd.DataFrame(constraint_data)
    df_constraints.to_csv(os.path.join(output_dir, f"{model.name}_constraints_and_slack_variables_primals.csv"), index=False)