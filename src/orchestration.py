import pyomo.environ as pyo
from src.data_store.coeff import STAGE
import src.constraint_store

def orchestrate_model(model):
    if STAGE == 1:
        # Build Objectives
        model.objective_registry = []
        for attr_name in dir(model):
            if "stage_1" in attr_name:
                attr = getattr(model, attr_name)
                if isinstance(attr, pyo.Expression):
                    model.objective_registry.append(attr)

        model.objective_function = pyo.Objective(
            expr=sum(model.objective_registry), 
            sense=pyo.maximize
        )

        # Build Constraints
        # find if src.constraint_store has functions whose name contains stage_1 
        # and add those functions as constraints to the model
        for attr_name in dir(src.constraint_store):
            if "stage_1" in attr_name and "constraint" in attr_name:
                attr = getattr(src.constraint_store, attr_name)
                if callable(attr):
                    constraint = pyo.Constraint(rule=attr)
                    # Strip _rule to give the constraint a clean name on the model
                    constraint_name = attr_name.replace("_rule", "")
                    setattr(model, constraint_name, constraint)
