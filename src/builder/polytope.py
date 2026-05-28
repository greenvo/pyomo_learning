import pyomo.environ as pyo
from src.datastore.coeff import STAGE

def build_model():
    if STAGE == 1:
        return pyo.ConcreteModel()
    return None
