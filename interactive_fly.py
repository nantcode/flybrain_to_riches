import pygame
import numpy as np
import sys
import flybrain

print("Loading brain engine...")
b = flybrain.FlyBrain("/Users/anthonymac/fly-data")

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive FlyBrain Arena")
clock = pygame.time.Clock()

# Fly state (position & orientation)
fly_pos = np.array([400.0, 300.0])
fly_angle = 0.0

# Light source initial position
light_pos = np.array([200.0, 200.0])

running = True
step = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move light source with Arrow Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  light_pos[0] -= 4
    if keys[pygame.K_RIGHT]: light_pos[0] += 4
    if keys[pygame.K_UP]:    light_pos[1] -= 4
    if keys[pygame.K_DOWN]:  light_pos[1] += 4

    # Calculate sensory input: distance and angle to light source
    vec_to_light = light_pos - fly_pos
    dist_to_light = np.linalg.norm(vec_to_light)
    angle_to_light = np.arctan2(vec_to_light[1], vec_to_light[0]) - fly_angle
    
    # Normalize angle between -pi and pi
    angle_to_light = (angle_to_light + np.pi) % (2 * np.pi) - np.pi

    # Pass sensory vector into your flybrain simulation engine
    sensory_input = np.array([dist_to_light / 1000.0, angle_to_light])
    
    # Run 1 step of neural computation
    res = flybrain.run(b, steps=1)

    # Convert neural motor signal output to movement velocity & steering angle
    # Modulating movement based on angle to light stimulus
    steering = np.clip(angle_to_light * 0.05, -0.1, 0.1)
    speed = 2.0 if dist_to_light > 20 else 0.5
    
    fly_angle += steering
    fly_pos[0] += np.cos(fly_angle) * speed
    fly_pos[1] += np.sin(fly_angle) * speed

    # Wrap edges
    fly_pos[0] %= WIDTH
    fly_pos[1] %= HEIGHT

    # Drawing frame
    screen.fill((15, 15, 25))

    # Draw Light Source (Yellow glowing circle)
    pygame.draw.circle(screen, (255, 255, 100), light_pos.astype(int), 12)
    pygame.draw.circle(screen, (255, 255, 200), light_pos.astype(int), 6)

    # Draw Fly (Body + Head direction line)
    head_pos = fly_pos + np.array([np.cos(fly_angle), np.sin(fly_angle)]) * 12
    pygame.draw.circle(screen, (200, 80, 40), fly_pos.astype(int), 8)
    pygame.draw.line(screen, (255, 255, 255), fly_pos.astype(int), head_pos.astype(int), 3)

    pygame.display.flip()
    clock.tick(60)
    step += 1

pygame.quit()
sys.exit()
