import pygame
import sys
import math
import random

pygame.init()

# Constants
canvas_width = 700 
canvas_height = 600

frame_rate = 60 #frame per second

trapper_count = 15
trapped_count = 20
trap_radius = 200
trapped_speed = 2
particle_size = 8

# Color choice
screen_color = 'black'
static_color = 'red'
mobile_color = 'yellow'

# Canvas
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Plasmatrap Simulation")

# Creating the trapping (static) particles in an equidistant circular order
static_particles = []
for i in range(trapper_count):
    posx = canvas_width // 2 + int(trap_radius * math.cos(2 * math.pi * i / trapper_count))
    posy = canvas_height // 2 + int(trap_radius * math.sin(2 * math.pi * i / trapper_count))
    static_particles.append([posx,posy])

# scattering the mobile particles within the trap in a random distance from the center
mobile_particles = []
for i in range(trapped_count):
    posx = canvas_width // 2 + random.randint(-trap_radius, trap_radius)
    posy = canvas_height // 2 + random.randint(-trap_radius, trap_radius)
    mobile_particles.append([posx,posy])

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    ## Drawing        
    screen.fill(screen_color)
    for particle in static_particles:
        pygame.draw.circle(screen, static_color, particle, particle_size)

    for particle in mobile_particles:
        print(particle)
        pygame.draw.circle(screen, mobile_color, particle, particle_size)
    
    pygame.display.flip()
    pygame.time.Clock().tick(frame_rate)

