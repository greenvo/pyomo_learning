import pyomo.environ as pyo
from src.datastore.var_bounds import X1_STAGE1_LOWER_BOUND, X1_STAGE1_UPPER_BOUND

def add_x1_stage1(model):
    model.x1 = pyo.Var(domain=pyo.Reals, bounds=(X1_STAGE1_LOWER_BOUND, X1_STAGE1_UPPER_BOUND))
