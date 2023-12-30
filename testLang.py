import numpy as np
import pylab as pl
from scipy.integrate import odeint

# Constants
canvas_width = 700 
canvas_height = 700


trapper_count = 15
trapped_count = 5
# trap_radius = 200
trap_radius = 0.8 * 1e-11
trapped_speed = 2
tr_particle_size = 10
td_particle_size = 5

q_trapped = -4.8e-10 #charge
charge_scale = 2
q_trapper = charge_scale*q_trapped
m_trapped = 1.6e-27 * 1e-3 #mass

dt = 1e-24 # time resolution

scale = 1e-11

def mtmRate(pos):
    pdots = np.zeros((len(pos),2))
    for i, pos_i in enumerate(pos):
        # against the peers
        vec_ip = np.delete(pos, i, 0) - pos_i
        pscaler = q_trapped**2/np.linalg.norm(vec_ip, axis=1)**3
        pterm = vec_ip * np.column_stack((pscaler, pscaler))
        # against the trappers
        vec_it = pos_trpr-pos_i
        tscaler = q_trapper*q_trapped/np.linalg.norm(vec_it, axis=1)**3
        tterm = vec_it * np.column_stack((tscaler,tscaler))

        pdots[i] = np.sum(pterm,0)+np.sum(tterm,0)
    return -pdots

    
ang_trpr = np.arange(trapper_count)*2*np.pi/trapper_count
pos_trpr = trap_radius * np.column_stack((np.cos(ang_trpr), np.sin(ang_trpr)))
# pos_trapper = transform(pos_trpr)


pos_real = np.zeros((trapped_count, 2))
radiuss = np.random.rand(trapped_count)*trap_radius
thetaas = np.random.rand(trapped_count)*2*np.pi
pos_real = np.column_stack((radiuss*np.cos(thetaas), radiuss*np.sin(thetaas)))

mtm_trapped = np.zeros((trapped_count, 2))
clrs = ['y', 'b', 'g', 'c', 'purple']
pl.close('all')
pl.figure(figsize=(4,4))
pl.plot(pos_trpr[:,0], pos_trpr[:,1], 'ro', ms=10)
for i in range(50):
    pl.scatter(pos_real[:,0], pos_real[:,1], marker='o', c=clrs, s=2)
    pl.xlim(-scale, scale)
    pl.ylim(-scale, scale)
    pl.savefig("%d.pdf"%i, format="pdf")
    pl.show()
        
    ## simple Euler method    
    pdots = mtmRate(pos_real)
    mtm_trapped += dt*pdots
    pos_real += dt*mtm_trapped/m_trapped
    escaped = trap_radius-np.linalg.norm(pos_real, axis=1)
    escaped = len(np.where(escaped<0)[0])
    print(i, escaped)
    print()
    
    
    
    
    
    
