import pyomo.environ as pyo
from src.datastore.var_bounds import X2_STAGE1_LOWER_BOUND, X2_STAGE1_UPPER_BOUND

def add_x2_stage1(model):
    model.x2 = pyo.Var(domain=pyo.Reals, bounds=(X2_STAGE1_LOWER_BOUND, X2_STAGE1_UPPER_BOUND))
