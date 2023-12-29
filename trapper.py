import pygame
import sys
import numpy as np

pygame.init()

# Constants
canvas_width = 700 
canvas_height = 700

frame_rate = 60 #frame per second

trapper_count = 15
trapped_count = 5
# trap_radius = 200
trap_radius = 0.8 * 1e-11
trapped_speed = 2
tr_particle_size = 10
td_particle_size = 5


# Color choice
screen_color = 'black'
static_color = 'red'
mobile_color = 'yellow'

q_trapped = -4.8e-10 #charge
charge_scale = 2
q_trapper = charge_scale*q_trapped
m_trapped = 1.67e-30 #mass in grams

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
    return pdots
    

def transform(pos, opt):
    pdiag_vec = np.array([2*scale, 2*scale]) #from (-c,-c) to (c,c)
    sdiag_vec = np.array([canvas_width, canvas_height])

    sbleft = -sdiag_vec/2 # bottom left corner coordinate
    ## assuming diag vectors in standard position:
    if opt=="to_screen":
        return pos*sdiag_vec/pdiag_vec  + sdiag_vec/2
    elif opt=="to_micro":
        return (pos-sdiag_vec/2)*pdiag_vec/sdiag_vec # first term: bottom left coord
        # return (pos-sdiag_vec/2)*sdiag_vec/pdiag_vec
    else:
        return None
    
# def transform(vec, opt):
#     pdiag_vec = np.array([2*scale, 2*scale]) #from (-c,-c) to (c,c)
#     sdiag_vec = np.array([canvas_width, canvas_height])
#
#     sangle = np.arctan2(sdiag_vec[:1], sdiag_vec[1:])
#     pangle = np.arctan2(pdiag_vec[:1], pdiag_vec[1:])
#     normscale = np.linalg.norm(sdiag_vec)/ np.linalg.norm(pdiag_vec)
#     if opt=='to_screen':
#         vnorm = np.linalg.norm(vec, axis=1) * normscale
#         theta = np.arctan2(vec[:,0], vec[:,1]) + sangle - pangle
#         tpos = np.column_stack((vnorm*np.cos(theta), vnorm*np.sin(theta)))
#         tpos += sdiag_vec/2
#     elif opt=='to_micro':
#         vec-=sdiag_vec/2
#         vnorm = np.linalg.norm(vec, axis=1)/normscale
#         theta = np.arctan2(vec[:,0], vec[:,1]) + pangle - sangle
#         tpos = np.column_stack((vnorm*np.cos(theta), vnorm*np.sin(theta)))
#     else:
#         return None
#
#     return tpos
                    

# Canvas
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Plasmatrap Simulation")

# # Creating the trapping (static) particles in an equidistant circular order
# pos_trpr = np.zeros((trapper_count, 2)) #infinite mass
# for i in range(trapper_count):
#     # posx = canvas_width / 2 + trap_radius * np.cos(2 * np.pi * i / trapper_count)
#     # posy = canvas_height / 2 + trap_radius * np.sin(2 * np.pi * i / trapper_count)
#     posx = trap_radius * np.cos(2 * np.pi * i / trapper_count)
#     posy = trap_radius * np.sin(2 * np.pi * i / trapper_count)
#     pos_trpr[i] = [posx, posy]
#
#     # pygame.draw.circle(screen, static_color, [posx,posy], tr_particle_size) ### draw
ang_trpr = np.arange(trapper_count)*2*np.pi/trapper_count
pos_trpr = trap_radius * np.column_stack((np.cos(ang_trpr), np.sin(ang_trpr)))
pos_trapper = transform(pos_trpr, "to_screen") 
    

# initial random position of the trapped sprites 
pos_real = np.zeros((trapped_count, 2))
radiuss = np.random.rand(trapped_count)*trap_radius
thetaas = np.random.rand(trapped_count)*2*np.pi
pos_real = np.column_stack((radiuss*np.cos(thetaas), radiuss*np.sin(thetaas)))

mtm_trapped = np.zeros((trapped_count, 2))
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    ## simple Euler method
    pdots = mtmRate(pos_real)
    mtm_trapped += dt*pdots
    pos_real += dt*mtm_trapped/m_trapped
    
    ### magnify to screen canvas
    # pos_trapped = canvas_width*pos_real/scale/2
    pos_trapped = transform(pos_real, "to_screen")
    
    print ("positions", pos_trapped)
   
    screen.fill(screen_color)
    for trapper in pos_trapper:
        pygame.draw.circle(screen, static_color, trapper.tolist(), tr_particle_size) ### draw
    
    for particle in pos_trapped:
        print(particle)
        pygame.draw.circle(screen, mobile_color, particle.tolist(), td_particle_size)
    
    pygame.display.flip()
    pygame.time.Clock().tick(frame_rate)



# def mtmRate(pos):
#     # estimate of pdot, rate of momentum
#     pdots = np.zeros((len(pos),2))
#     for i, pos_i in enumerate(pos):
#         # with peers
#         vec_ip = np.delete(pos, i, 0) - pos_i
#         pscaler = q_trapped**2/np.sqrt(np.sum(vec_ip**2, 1))**3
#         pscaler = np.column_stack((pscaler, pscaler))
#         wpeers = np.sum(pscaler * vec_ip, 0)
#         # with trappers
#         tpos_real = 2*scale/canvas_width*pos_trapper
#         vec_it = tpos_real-pos_i
#         tscaler = q_trapper*q_trapped/np.sqrt(np.sum(vec_it**2, 1))**3
#         tscaler = np.column_stack((tscaler, tscaler))
#         wtrapr = np.sum(tscaler * vec_it,0)
#
#         pdots[i] = wpeers+wtrapr
#     return pdots


 