import pygame
import math

# Define the arm segments and angles
segment_lengths = [100, 80, 60]
joint_angles = [45, -30, 20]  # Angles in degrees

pixel_scalar = 65

dim = (600, 400)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(dim)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 24)

base_pos = (dim[0]//2, dim[1]//2)

a_1 = 1
a_2 = 2
a_3 = 2
a_4 = 0.5

a_1 *= pixel_scalar
a_2 *= pixel_scalar
a_3 *= pixel_scalar
a_4 *= pixel_scalar

# Function to convert polar to Cartesian coordinates (adjusted for unit circle direction)
def polar_to_cartesian(length, angle, start_pos):
    x = start_pos[0] + length * math.cos(math.radians(-angle))
    y = start_pos[1] + length * math.sin(math.radians(-angle))
    return int(x), int(y)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    x_f = (mouse_pos[0] - base_pos[0])
    y_f = -(mouse_pos[1] - base_pos[1])

    gamma = math.atan2(y_f, x_f)
    gamma = -math.pi /2 
    
    try:
        x_w = x_f - (a_4 * math.cos(gamma))
        y_w = y_f - (a_4 * math.sin(gamma))

        r = math.sqrt((x_w ** 2) + (y_w ** 2))

        phi_2 = math.acos(((r ** 2) + (a_2 ** 2) - (a_3 ** 2)) / (2 * r * a_2))
        phi_1 = math.atan2(y_w, x_w)

        phi_3 = math.acos(((a_2 ** 2) + (a_3 ** 2) - (r ** 2)) / (2 * a_2 * a_3))

        # If x_f > 0, switch arm to elbow up position
        # does not currently work
        if x_f > 0:
            theta_1 = phi_1 + phi_2  # Change subtraction to addition
            theta_2 = -(math.pi - phi_3)  # Negate θ2 for elbow-up
        else:
            theta_1 = phi_1 - phi_2  # Default elbow-down
            theta_2 = math.pi - phi_3  # Default elbow-down
        # Compute theta_3 using the desired end-effector orientation
        theta_3 = gamma - (theta_1 + theta_2)

        # Define the arm segments and angles
        segment_lengths = [a_2, a_3, a_4]
        joint_angles = [math.degrees(theta_1), math.degrees(theta_2), math.degrees(theta_3)]  # Angles in degrees

    except Exception:
        theta_1 = 120
        theta_2 = -100
        theta_3 = -45
        segment_lengths = [a_2, a_3, a_4]
        joint_angles = [theta_1, theta_2, theta_3]

    screen.fill(WHITE)

    # Draw the robotic arm
    current_pos = base_pos
    total_angle = 0

    for i in range(len(segment_lengths)):
        total_angle += joint_angles[i]
        next_pos = polar_to_cartesian(segment_lengths[i], total_angle, current_pos)
        pygame.draw.line(screen, BLUE, current_pos, next_pos, 5)
        pygame.draw.circle(screen, RED, next_pos, 8)
        current_pos = next_pos

    # Draw base
    pygame.draw.circle(screen, RED, base_pos, 10)

    # Display end effector and target position
    end_effector_pos = current_pos


    # theta_add_text = font.render(f"theta add: {math.degrees(theta_1+theta_2+theta_3):.6}", True, BLACK)
    gamma_text = font.render(f"gamma: {math.degrees(math.atan2(y_f, x_f)):.6}", True, BLACK)
    end_effector_text = font.render(f"End Effector: {end_effector_pos}", True, BLACK)
    target_text = font.render(f"Target: {mouse_pos}", True, BLACK)
    theta_text = font.render(f"Theta 1: {round(joint_angles[0], 2)}°, Theta 2: {round(joint_angles[1], 2)}°, Theta 3: {round(joint_angles[2], 2)}°", True, BLACK)


    # screen.blit(theta_add_text, (10, dim[1]-110))
    screen.blit(gamma_text, (10, dim[1] - 90))
    screen.blit(end_effector_text, (10, dim[1] - 70))
    screen.blit(target_text, (10, dim[1] - 50))
    screen.blit(theta_text, (10, dim[1] - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()