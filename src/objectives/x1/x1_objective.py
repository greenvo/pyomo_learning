import pyomo.environ as pyo
from src.datastore.coeff import X1_STAGE1_OBJ_COEFF

def store_stage1_x1_objective(model):
    model.stage1_x1_expr = pyo.Expression(
        expr=X1_STAGE1_OBJ_COEFF * model.x1,
        doc="Objective contribution for x1 in Stage 1"
    )
