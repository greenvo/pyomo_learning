import pyomo.environ as pyo
from src.datastore.coeff import X2_STAGE1_OBJ_COEFF

def store_stage1_x2_objective(model):
    model.stage1_x2_expr = pyo.Expression(
        expr=X2_STAGE1_OBJ_COEFF * model.x2,
        doc="Objective contribution for x2 in Stage 1"
    )
