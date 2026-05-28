import pyomo.environ as pyo
import pkgutil
import importlib
import sys
from src.utils.logger_factory import setup_logger

logger = setup_logger(__name__, "orchestrator.log")

def _walk_and_import(path, prefix):
    for _, module_name, is_pkg in pkgutil.walk_packages(path, prefix + "."):
        importlib.import_module(module_name)

def build_objectives(model):
    import src.objectives
    logger.info("Discovering and building objectives...")
    _walk_and_import(src.objectives.__path__, "src.objectives")
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.objectives"):
            for attr_name in dir(mod):
                if attr_name.startswith("store_") and "objective" in attr_name:
                    func = getattr(mod, attr_name)
                    if callable(func):
                        logger.debug(f"Storing objective via {attr_name}")
                        func(model)

    logger.info("Assembling global objective function...")
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
