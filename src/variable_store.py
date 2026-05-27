import pyomo.environ as pyo
from src.data_store.var_bounds import *

def add_variables(model):
    model.x1 = pyo.Var(domain=pyo.Reals, bounds=(x1_stage_1_lower_bound, x1_stage_1_upper_bound))
    model.x2 = pyo.Var(domain=pyo.Reals, bounds=(x2_stage_1_lower_bound, x2_stage_1_upper_bound))
