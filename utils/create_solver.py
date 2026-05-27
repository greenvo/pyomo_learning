import pyomo.environ as pyo
from typing import Set

# =============================================================================
# STEP 1: IMMUTABLE DOMAIN VALIDATION ENFORCEMENTS
# =============================================================================
# Valid inputs are structured as sets to optimize membership check performance.
_VALID_PARAMS_FOR_PRESOLVE: Set[str] = {"on", "off"}
_VALID_PARAMS_FOR_SCALING: Set[str] = {"on", "off"}
_KNOWN_SOLVERS: Set[str] = {"appsi_highs", "cbc"}


def _validate_param_for_presolve(value: str, name: str) -> str:
    if value not in _VALID_PARAMS_FOR_PRESOLVE:
        raise ValueError(
            f"{name} has been given incorrect value {value!r}. "
            f"Must be {_VALID_PARAMS_FOR_PRESOLVE}."
        )
    return value


def _validate_param_for_scaling(value: str, name: str) -> str:
    if value not in _VALID_PARAMS_FOR_SCALING:
        raise ValueError(
            f"{name} has been given incorrect value {value!r}. "
            f"Must be {_VALID_PARAMS_FOR_SCALING}."
        )
    return value


def _validate_is_a_known_solver(value: str, name: str) -> str:
    if value not in _KNOWN_SOLVERS:
        raise ValueError(
            f"{name} has been given incorrect value {value!r}. "
            f"Must be {_KNOWN_SOLVERS}."
        )
    return value


# =============================================================================
# STEP 2: CORE SOLVER FACTORY CREATOR
# =============================================================================
def pyomo_solver_creator(
    solver_name: str = "appsi_highs",
    time_limit: int = 300,
    presolve: str = "on",
    scaling: str = "on"
) -> pyo.CommonSolverInterface:
    """
    Instantiates and configures a Pyomo solver object wrapper.
    1. Enforces strict input parameter verification before the solver binary runs.
    2. Maps generic inputs cleanly into solver-specific API option structures.
    3. Returns a consistent object interface supporting the .solve() execution pattern.
    """
    
    # Run the validation checks to fail immediately if an input is corrupt
    _validate_is_a_known_solver(solver_name, "solver_name")
    _validate_param_for_presolve(presolve, "presolve")
    _validate_param_for_scaling(scaling, "scaling")

    # Instantiate the dynamic solver component using the factory registry
    solver = pyo.SolverFactory(solver_name)

    # Inject the validated parameters directly into the internal options cache
    if solver_name == "appsi_highs":
        # Options translate directly to the highspy C++ API properties
        solver.options['time_limit'] = float(time_limit)
        solver.options['presolve'] = presolve
        solver.options['simplex_scale_strategy'] = 1 if scaling == "on" else 0

    elif solver_name == "cbc":
        # COIN-OR CBC specific structural overrides
        solver.options['sec'] = time_limit
        if presolve == "on":
            solver.options['presolve'] = ""

    return solver