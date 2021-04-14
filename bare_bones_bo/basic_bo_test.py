import epics
from test_emit_no_ctrl_class import *
from bayes_opt import BayesianOptimization


em = Emit_Meas()
emit = em.launch_emittance_measurment()

pvname_1 = 'SOLN:IN20:121:BCTRL' #solenoid
pvname_2 = 'QUAD:IN20:121:BCTRL' #skew quad
pvname_3 = 'QUAD:IN20:122:BCTRL' #skew qaud


def evaluate(varx,vary,varz):

    #epics.caput(pvname_1,varx)
    #epics.caput(pvname_2,vary)
    #epics.caput(pvname_3,varz)
 

    return -1*objective()


def objective():
    
    emit = em.launch_emittance_measurment()
    
    return np.array(emit)


pbounds = {'varx': (0.44, 0.55),
           'vary': (-0.02, 0.02),
           'varz': (-0.02, 0.02)}

optimizer = BayesianOptimization(
    f = evaluate,
    pbounds = pbounds,
    random_state = 1,
)

optimizer.maximize(
    init_points=5,
    n_iter=10,
)




SOL_opt = optimizer.max['params']['varx']
CQ_opt = optimizer.max['params']['vary']
SQ_opt = optimizer.max['params']['varz']
print('optimum (pv_units) ',SOL_opt, CQ_opt, SQ_opt)

opt_emit = -1*optimizer.max['target']
print('optimum geom emit ', opt_emit)
