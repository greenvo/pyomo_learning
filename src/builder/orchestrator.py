import pyomo.environ as pyo
from src.datastore.coeff import STAGE
import pkgutil
import importlib
import sys

def _walk_and_import(path, prefix):
    for _, module_name, is_pkg in pkgutil.walk_packages(path, prefix + "."):
        importlib.import_module(module_name)

def orchestrate_model(model):
    if STAGE != 1:
        return

    # Dynamically find and call all variable store functions
    import src.variables
    _walk_and_import(src.variables.__path__, "src.variables")
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.variables"):
            for attr_name in dir(mod):
                if attr_name.startswith("add_"):
                    func = getattr(mod, attr_name)
                    if callable(func):
                        func(model)

    # Dynamically find and call all objective store functions
    import src.objectives
    _walk_and_import(src.objectives.__path__, "src.objectives")
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.objectives"):
            for attr_name in dir(mod):
                if attr_name.startswith("store_") and "objective" in attr_name:
                    func = getattr(mod, attr_name)
                    if callable(func):
                        func(model)

    # Build Objective Function
    model.objective_registry = []
    for attr_name in dir(model):
        if "stage1" in attr_name:
            attr = getattr(model, attr_name)
            if isinstance(attr, pyo.Expression):
                model.objective_registry.append(attr)

    model.objective_function = pyo.Objective(
        expr=sum(model.objective_registry), 
        sense=pyo.maximize
    )

    # Dynamically build constraints
    import src.constraints
    _walk_and_import(src.constraints.__path__, "src.constraints")
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.constraints"):
            for attr_name in dir(mod):
                if "stage1" in attr_name and "constraint_rule" in attr_name:
                    attr = getattr(mod, attr_name)
                    if callable(attr):
                        constraint = pyo.Constraint(rule=attr)
                        constraint_name = attr_name.replace("_rule", "")
                        setattr(model, constraint_name, constraint)
