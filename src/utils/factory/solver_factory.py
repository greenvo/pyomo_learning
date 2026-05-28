import pyomo.environ as pyo
from typing import Set

# =============================================================================
# STEP 1: IMMUTABLE DOMAIN VALIDATION ENFORCEMENTS
# =============================================================================
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
    ):
    
    _validate_is_a_known_solver(solver_name, "solver_name")
    _validate_param_for_presolve(presolve, "presolve")
    _validate_param_for_scaling(scaling, "scaling")

    solver = pyo.SolverFactory(solver_name)

    if solver_name == "appsi_highs":
        solver.options['time_limit'] = float(time_limit)
        solver.options['presolve'] = presolve
        solver.options['simplex_scale_strategy'] = 1 if scaling == "on" else 0
    elif solver_name == "cbc":
        solver.options['sec'] = time_limit
        if presolve == "on":
            solver.options['presolve'] = ""

    return solver
