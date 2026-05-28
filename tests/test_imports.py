import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestImports(unittest.TestCase):
    def test_datastore_imports(self):
        from src.datastore.coeff import STAGE
        from src.datastore.var_bounds import X1_STAGE1_LOWER_BOUND
        self.assertEqual(STAGE, 1)

    def test_constraints_imports(self):
        from src.constraints.stage1.c1.c1_constraint import add_c1_stage1_constraint_rule
        self.assertTrue(callable(add_c1_stage1_constraint_rule))

    def test_objectives_imports(self):
        from src.objectives.x1.x1_objective import store_stage1_x1_objective
        self.assertTrue(callable(store_stage1_x1_objective))

    def test_variables_imports(self):
        from src.variables.x1.add_x1 import add_x1_stage1
        self.assertTrue(callable(add_x1_stage1))

    def test_utils_imports(self):
        from src.utils.factory.solver_factory import pyomo_solver_creator
        self.assertTrue(callable(pyomo_solver_creator))

if __name__ == '__main__':
    unittest.main()
