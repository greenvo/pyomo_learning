from src.datastore.coeff import *

def add_c1_stage1_constraint_rule(m):
    return C1_DATA_X1_STAGE1 * m.x1 + C1_DATA_X2_STAGE1 * m.x2 <= C1_RHS_STAGE1
