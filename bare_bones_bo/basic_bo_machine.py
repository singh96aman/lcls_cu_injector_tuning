import epics
from emit_ctrl_class import *
from bayes_opt import BayesianOptimization
import time


em = Emit_Meas()
emit = em.launch_emittance_measurment()

pvname_1 = 'SOLN:IN20:121:BCTRL' #solenoid
pvname_2 = 'QUAD:IN20:121:BCTRL' #skew quad
pvname_3 = 'QUAD:IN20:122:BCTRL' #skew qaud

#matching quads
pvname_4 = 'QUAD:IN20:525:BCTRL' #Q525
pvname_5 = 'QUAD:IN20:511:BCTRL' #Q511
pvname_6 = 'QUAD:IN20:441:BCTRL' #Q441
pvname_7 = 'QUAD:IN20:425:BCTRL' #Q425
pvname_8 = 'QUAD:IN20:371:BCTRL' #Q371
pvname_9 = 'QUAD:IN20:361:BCTRL' #Q361

def evaluate(varx,vary,varz,var4,var5,var6,var7,var8,var9):

    epics.caput(pvname_1,varx)
    epics.caput(pvname_2,vary)
    epics.caput(pvname_3,varz)
    epics.caput(pvname_4,var4)
    epics.caput(pvname_5,var5)
    epics.caput(pvname_6,var6)
    epics.caput(pvname_7,var7)
    epics.caput(pvname_8,var8)
    epics.caput(pvname_9,var9)
    
    time.sleep(3)
    

    return -1*objective()


def objective():
    
    emit = em.launch_emittance_measurment()
    
    return np.array(emit)


pbounds = {'varx': (0.44, 0.55),
           'vary': (-0.02, 0.02),
           'varz': (-0.02, 0.02),
           'var4': (-5.0, -3.0),
           'var5': (2.0, 7.0),
           'var6': (-1.0, 2.0),
           'var7': (-4.0, -1.0),
           'var8': (2.5, 2.9),
           'var9': (-3.5, -2.75),
          }

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
Q525_opt = optimizer.max['params']['var4']
Q511_opt = optimizer.max['params']['var5']
Q441_opt = optimizer.max['params']['var6']
Q425_opt = optimizer.max['params']['var7']
Q371_opt = optimizer.max['params']['var8']
Q361_opt = optimizer.max['params']['var9']
print('optimum (pv_units) ',SOL_opt, CQ_opt, SQ_opt)
print('matching quads optimum (pv_units) ',Q525_opt, Q511_opt, Q441_opt, Q425_opt, Q371_opt, Q361_opt)

opt_emit = -1*optimizer.max['target']
print('optimum geom emit ', opt_emit)
