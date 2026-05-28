import pyomo.environ as pyo
import pkgutil
import importlib
import sys
from src.utils.logger_factory import setup_logger

logger = setup_logger(__name__, "orchestrator.log")

def _walk_and_import(path, prefix):
    for _, module_name, is_pkg in pkgutil.walk_packages(path, prefix + "."):
        importlib.import_module(module_name)

def build_constraints(model):
    import src.constraints
    logger.info("Discovering and building constraints...")
    _walk_and_import(src.constraints.__path__, "src.constraints")
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.constraints"):
            for attr_name in dir(mod):
                if "stage1" in attr_name and "constraint_rule" in attr_name:
                    attr = getattr(mod, attr_name)
                    if callable(attr):
                        logger.debug(f"Building constraint via {attr_name}")
                        constraint = pyo.Constraint(rule=attr)
                        constraint_name = attr_name.replace("_rule", "")
                        setattr(model, constraint_name, constraint)
