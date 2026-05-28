from src.datastore.coeff import *

def add_c2_stage1_constraint_rule(m):
    return C2_DATA_X1_STAGE1 * m.x1 + C2_DATA_X2_STAGE1 * m.x2 <= C2_RHS_STAGE1
