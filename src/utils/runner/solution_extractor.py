import pyomo.environ as pyo
from src.datastore.coeff import STAGE

def add_solution_extraction(model):
    if STAGE == 1:
        model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
        model.rc = pyo.Suffix(direction=pyo.Suffix.IMPORT)
