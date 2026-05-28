"""
tests/test_imports.py
---------------------
Verifies that every library declared in pyproject.toml is correctly
installed and importable within the Poetry virtual environment.
"""

import importlib
import sys


# ---------------------------------------------------------------------------
# Map: human-readable name  ->  import name (they can differ, e.g. highspy)
# ---------------------------------------------------------------------------
REQUIRED_LIBRARIES = {
    # Core scientific computing
    "numpy":       "numpy",
    "pandas":      "pandas",
    "scipy":       "scipy",

    # Pyomo optimisation
    "pyomo":       "pyomo",

    # HiGHS solver
    "highspy":     "highspy",

    # Plotting & visualisation
    "matplotlib":  "matplotlib",
    "seaborn":     "seaborn",

    # Utilities
    "openpyxl":    "openpyxl",
    "jupyterlab":  "jupyterlab",
}


def check_library(package_name: str, import_name: str) -> dict:
    """Try to import a library and return a result dict."""
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, "__version__", "version unavailable")
        return {"package": package_name, "status": "OK", "version": version, "error": None}
    except ImportError as exc:
        return {"package": package_name, "status": "MISSING", "version": "-", "error": str(exc)}
    except Exception as exc:
        return {"package": package_name, "status": "ERROR", "version": "-", "error": str(exc)}


def run_checks() -> bool:
    """Run all import checks and print a formatted report. Returns True if all pass."""
    print("\n" + "=" * 60)
    print("  Library Import Check")
    print(f"  Python: {sys.version}")
    print("=" * 60)

    col_w = {"package": 14, "status": 9, "version": 16}
    header = (
        f"  {'Package':<{col_w['package']}}"
        f"{'Status':<{col_w['status']}}"
        f"{'Version':<{col_w['version']}}"
        f"Notes"
    )
    print(header)
    print("  " + "-" * 56)

    results = [check_library(pkg, imp) for pkg, imp in REQUIRED_LIBRARIES.items()]

    for r in results:
        status_icon = "[OK]" if r["status"] == "OK" else "[!!]"
        notes = r["error"] if r["error"] else ""
        print(
            f"  {status_icon} {r['package']:<{col_w['package'] - 4}}"
            f"{r['status']:<{col_w['status']}}"
            f"{r['version']:<{col_w['version']}}"
            f"{notes}"
        )

    print("=" * 60)

    failed = [r for r in results if r["status"] != "OK"]
    if not failed:
        print(f"  [OK] All {len(results)} libraries imported successfully.\n")
        return True
    else:
        print(f"  [!!] {len(failed)} library/libraries failed to import:")
        for r in failed:
            print(f"      - {r['package']}: {r['error']}")
        print()
        return False


# ---------------------------------------------------------------------------
# pytest-compatible individual test functions
# ---------------------------------------------------------------------------

def _make_test(pkg, imp):
    """Factory that returns a pytest test function for one library."""
    def test_fn():
        result = check_library(pkg, imp)
        assert result["status"] == "OK", (
            f"Could not import '{imp}' (package: '{pkg}'). "
            f"Error: {result['error']}"
        )
    test_fn.__name__ = f"test_import_{pkg.replace('-', '_')}"
    return test_fn


# Dynamically create one test_* function per library so pytest reports them individually
for _pkg, _imp in REQUIRED_LIBRARIES.items():
    globals()[f"test_import_{_pkg.replace('-', '_')}"] = _make_test(_pkg, _imp)


# ---------------------------------------------------------------------------
# Direct execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
