import pyomo.environ as pyo
import pkgutil
import importlib
import sys
from src.utils.logger_factory import setup_logger

logger = setup_logger(__name__, "orchestrator.log")

def _walk_and_import(path, prefix):
    for _, module_name, is_pkg in pkgutil.walk_packages(path, prefix + "."):
        importlib.import_module(module_name)

def build_variables(model):
    import src.variables
    logger.info("Discovering and building variables...")
    _walk_and_import(src.variables.__path__, "src.variables")
    for mod_name, mod in sys.modules.items():
        if mod_name.startswith("src.variables"):
            for attr_name in dir(mod):
                if attr_name.startswith("add_"):
                    func = getattr(mod, attr_name)
                    if callable(func):
                        logger.debug(f"Adding variable via {attr_name}")
                        func(model)
