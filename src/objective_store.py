import pyomo.environ as pyo
from src.data_store.coeff import X1_stage_1_objective_coefficient, X2_stage_1_objective_coefficient

def store_objectives(model):
    model.stage_1_x1_expr = pyo.Expression(
        expr=X1_stage_1_objective_coefficient * model.x1,
        doc="Objective contribution for x1 in Stage 1"
    )
    
    model.stage_1_x2_expr = pyo.Expression(
        expr=X2_stage_1_objective_coefficient * model.x2,
        doc="Objective contribution for x2 in Stage 1"
    )
