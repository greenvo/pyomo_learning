from src.data_store.coeff import *

def add_c1__stage_1_constraint_rule(m):
    return C1_data_x1_stage_1*m.x1 + C1_data_x2_stage_1*m.x2 <= C1_rhs_stage_1

def add_c2_stage_1_constraint_rule(m):
    return C2_data_x1_stage_1*m.x1 + C2_data_x2_stage_1*m.x2 <= C2_rhs_stage_1
