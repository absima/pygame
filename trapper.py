import pygame
import sys
import numpy as np

pygame.init()

# Constants
canvas_width = 700 
canvas_height = 600

frame_rate = 60 #frame per second

trapper_count = 15
trapped_count = 20
trap_radius = 200
trapped_speed = 2
tr_particle_size = 10
td_particle_size = 5

# Color choice
screen_color = 'black'
static_color = 'red'
mobile_color = 'yellow'

q_trapped = -4.8e-10 #charge
q_trapper = 2*q_trapped
m_trapped = 1.6e-27 * 1e-3 #mass

dt = 1e-24 # time resolution


# Canvas
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Plasmatrap Simulation")

# Creating the trapping (static) particles in an equidistant circular order
pos_trapper = np.zeros((trapper_count, 2)) #infinite mass
for i in range(trapper_count):
    posx = canvas_width // 2 + int(trap_radius * np.cos(2 * np.pi * i / trapper_count))
    posy = canvas_height // 2 + int(trap_radius * np.sin(2 * np.pi * i / trapper_count))
    pos_trapper[i] = [posx, posy]
    
    pygame.draw.circle(screen, static_color, [posx,posy], tr_particle_size) ### draw
    

# initial random position of the trapped sprites 
pos_trapped = np.zeros((trapped_count, 2))
for i in range(trapped_count):
    radius_i = np.random.rand()*trap_radius
    theta_i = np.random.rand()*2*np.pi    
    posx = canvas_width // 2 + int(radius_i * np.cos(theta_i))
    posy = canvas_height // 2 + int(radius_i * np.sin(theta_i))
    pos_trapped[i]=[posx,posy]

mtm_trapped = np.zeros((trapped_count, 2))

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for particle in pos_trapped:
        print(particle)
        pygame.draw.circle(screen, mobile_color, particle.tolist(), td_particle_size)
    
    pygame.display.flip()
    pygame.time.Clock().tick(frame_rate)

