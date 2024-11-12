import pygame
import random

# Initialize Pygame and the mixer for audio
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the background image
background = pygame.image.load(r"C:\Users\Frank Kunda\Downloads\Game_Background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and play background music
pygame.mixer.music.load(r"C:\Users\Frank Kunda\PycharmProjects\game2\CG GAME\lil baby.mp3")
pygame.mixer.music.play(-1)  # Play the music indefinitely (loop)

# Function to load character frames with resizing
def load_character_frames(frame_count, new_size=(75, 75)):
    frames = []
    for i in range(1, frame_count + 1):
        file_path = fr"C:\Users\Frank Kunda\PycharmProjects\game2\CG GAME\frames\frame{i}.gif"
        frame = pygame.image.load(file_path)
        frame = pygame.transform.scale(frame, new_size)  # Resize the frame
        frames.append(frame)
    return frames

# Load character frames
character_frames = load_character_frames(6, new_size=(75, 75))  # Set the desired size here
frame_index = 0
frame_rate = 0.15  # Adjusted frame rate for smoother animation
frame_counter = 0

# Player settings
player = pygame.Rect(100, 450, 75, 75)  # Adjust player's size to match character size
player_speed = 10
gravity = 0.5
jump_speed = -10
player_velocity_y = 0
is_jumping = False
GROUND_HEIGHT = 450  # Set the ground height

# Load obstacle GIF
def load_obstacle_image(file_path, new_size=(40, 40)):
    obstacle_image = pygame.image.load(file_path)
    obstacle_image = pygame.transform.scale(obstacle_image, new_size)  # Resize if necessary
    return obstacle_image

# Load the obstacle GIF
obstacle_image_path = r"C:\Users\Frank Kunda\PycharmProjects\game2\CG GAME\obstacle.gif"
obstacle_image = load_obstacle_image(obstacle_image_path, new_size=(40, 40))  # Set size to match image

# Obstacles
obstacles = []

# Background position and speed
bg_x1 = 0
bg_x2 = SCREEN_WIDTH
bg_speed = 5  # Initial background speed

# Score variable and font
score = 0
font = pygame.font.Font(None, 36)  # Use default font with size 36

# Track the last score threshold for speed increase
last_speed_increase_score = 0

# Game variables
running = True
clock = pygame.time.Clock()

def game_loop():
    global score
    global player_velocity_y
    global is_jumping
    global obstacles
    global frame_index
    global frame_counter
    global bg_speed
    global last_speed_increase_score

    score = 0
    player_velocity_y = 0
    is_jumping = False
    obstacles = []
    frame_index = 0
    frame_counter = 0

    running = True
    while running:
        # Move background
        global bg_x1, bg_x2
        bg_x1 -= bg_speed
        bg_x2 -= bg_speed

        # Reset background position
        if bg_x1 <= -SCREEN_WIDTH:
            bg_x1 = SCREEN_WIDTH
        if bg_x2 <= -SCREEN_WIDTH:
            bg_x2 = SCREEN_WIDTH

        # Check for speed increase based on score
        if score >= last_speed_increase_score + 100:  # Check if score crossed the next threshold
            bg_speed += 0.5  # Increase the speed by 0.5
            last_speed_increase_score += 100  # Update the last threshold reached

        # Display the background
        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))

        # Capture events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Player movement with boundary checks
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.width:
            player.x += player_speed

        # Handle jumping
        if not is_jumping and keys[pygame.K_SPACE]:
            is_jumping = True
            player_velocity_y = jump_speed

        if is_jumping:
            player_velocity_y += gravity
            player.y += player_velocity_y
            if player.y >= GROUND_HEIGHT:
                player.y = GROUND_HEIGHT
                is_jumping = False

        # Add obstacles randomly
        if random.randint(1, 50) == 1:
            obstacle_y = GROUND_HEIGHT - 50  # Ensure the obstacle is at the correct height
            obstacles.append(pygame.Rect(800, 470, 40, 40))  # Use the correct obstacle size

        # Move obstacles and detect collision
        for obstacle in obstacles[:]:  # Iterate over a copy of obstacles list to safely modify it
            obstacle.x -= player_speed
            screen.blit(obstacle_image, obstacle.topleft)  # Draw the obstacle image

            # Check if the obstacle has passed the player without a collision
            if obstacle.x + obstacle.width < player.x:
                score += 10  # Increment score when player avoids the obstacle
                obstacles.remove(obstacle)  # Remove the obstacle from the list

            # Check for collision
            if player.colliderect(obstacle):
                return end_screen()  # Trigger end screen when collision happens

        # Remove obstacles that have moved off-screen
        obstacles = [ob for ob in obstacles if ob.x > -50]  # Adjusted to match the obstacle width

        # Animate character
        if not is_jumping:
            frame_counter += frame_rate
            if frame_counter >= 1:
                frame_counter = 0
                frame_index = (frame_index + 1) % len(character_frames)

        # Draw player
        screen.blit(character_frames[frame_index], player.topleft)

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White color for the score
        screen.blit(score_text, (10, 10))  # Position the score in the top left corner

        # Update the screen
        pygame.display.update()

        # Control the frame rate
        clock.tick(30)

def end_screen():
    while True:
        screen.fill((0, 0, 0))  # Clear the screen with black

        # Display final score
        game_over_text = font.render(f"Game Over! Your Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))

        # Display options
        replay_text = font.render("Press 'P' to Play Again or 'E' to Exit", True, (255, 255, 255))
        screen.blit(replay_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

        # Update display
        pygame.display.update()

        # Capture events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to play again
                    return game_loop()
                if event.key == pygame.K_e:  # Press 'E' to exit
                    pygame.quit()
                    quit()

# Start the game loop
game_loop()

# Quit Pygame
pygame.quit()
