# wl_abstract_callback.py: AbstractModel with Callback for post processing
from pyomo.environ import *

model = AbstractModel()
model.name = "(WL)"

model.N = Set()
model.M = Set()

model.d = Param(model.N,model.M)
model.P = Param()

model.x = Var(model.N, model.M, bounds=(0,1))
model.y = Var(model.N, within=Binary)

def obj_rule(model):
    return sum(model.d[n,m]*model.x[n,m] for n in model.N for m in model.M)
model.obj = Objective(rule=obj_rule)

def one_per_cust_rule(model, m):
    return sum(model.x[n,m] for n in model.N) == 1
model.one_per_cust = Constraint(model.M, rule=one_per_cust_rule)

def warehouse_active_rule(model, n, m):
    return model.x[n,m] <= model.y[n]
model.warehouse_active = Constraint(model.N, model.M, rule=warehouse_active_rule)

def num_warehouses_rule(model):
    return sum(model.y[n] for n in model.N) <= model.P
model.num_warehouses = Constraint(rule=num_warehouses_rule)

# @callback:
def pyomo_postprocess(options=None, instance=None, \
                      results=None):
    print('***')
    for wl in instance.y:
        if value(instance.y[wl]) > 0.5:
            customers = [str(cl) for cl in instance.M if value(instance.x[wl, cl] > 0.5)]
            print(str(wl), 'serves customers:', customers)
        else:
            print(str(wl)+": do not build")
    print('***')
# @:callback

