import pygame
import random
import os
import time
import sys
from moviepy.editor import VideoFileClip
from ffpyplayer.player import MediaPlayer


# Initialize Pygame
pygame.init()

# Adjust the mixer settings for better performance
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error initializing Pygame mixer: {e}")

dark_mode = False
difficulty = "Medium"

# Screen dimensions
screen_width = 850
screen_height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
gray=(128,128,128)
dark_gray=(169,169,169)
snow=(255,250,250)

# Brighter and more diverse colors
orange = (255, 165, 0)  # Bright orange
purple = (176, 38, 255)  # glowing purple
teal = (0, 128, 128)  # Teal blue
pink = (255, 192, 203)  # Light pink
lime = (0, 255, 127)  # Bright lime green

# Buttons
BUTTON_COLOR = (0, 128, 255)  # Vibrant blue
BUTTON_HOVER_COLOR = (0, 255, 128)  # Lighter green

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Match Mania')

# Global dictionaries for storing images
alphabet_images = {}
compare_images = {}

# Define folders
symbol_folders = [f'images_{i}' for i in range(1, 6)]
# math_symbol_folders=[f'images_{i}' for i in range(6,8)]
# number_folders = [f'images_{i}' for i in range(8,11)] changes thre funtion to call the main main_number_folder instead 
# 1 number folder named all_nums for 11 to 14 
font_folders = [f'images_{i}' for i in range(15, 22)]
# u need images_26 for hindi
# hindi_alphabet_folder = [f'images_{i}' for i in range(22, 29)]

# Define main folders
main_image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_alphabet_images')
main_symbol_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_symbol_images')
main_word_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_word_images')
main_number_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_number_images')
main_math_symbol_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_math_symbols')

image_size = (100, 100)  # Resize images to this size

# Initialize video playback variables
video = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video.mp4')
is_playing = True
video_speed = 1.0

def play_video(video_path):
    global is_playing, video_speed

    # Load video using ffpyplayer
    player = MediaPlayer(video_path)
    clock = pygame.time.Clock()

    # Define buttons
    backward_button = pygame.Rect(screen_width // 2 - 280, screen_height - 70, 100, 50)
    play_pause_button = pygame.Rect(screen_width // 2 - 160, screen_height - 70, 100, 50)
    forward_button = pygame.Rect(screen_width // 2 - 40, screen_height - 70, 100, 50)
    speed_button = pygame.Rect(screen_width // 2 + 80, screen_height - 70, 100, 50)
    back_button = pygame.Rect(screen_width // 2 + 200, screen_height - 70, 100, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_pause_button.collidepoint(event.pos):
                    is_playing = not is_playing
                elif forward_button.collidepoint(event.pos):
                    player.seek(10)  # Seek forward 10 seconds
                elif backward_button.collidepoint(event.pos):
                    player.seek(-10)  # Seek backward 10 seconds
                elif speed_button.collidepoint(event.pos):
                    video_speed = 2.0 if video_speed == 1.0 else 1.0
                    
                elif back_button.collidepoint(event.pos):
                    player.close_player()
                    return  # Go back to the instruction screen

        if is_playing:
            frame, val = player.get_frame()
            if val == 'eof':
                player.seek(0)  # Restart video on end
            if frame is not None:
                img, t = frame
                # Convert frame to Pygame surface
                frame_surface = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), "RGB")
                
                # Scale the video to fit the screen (600x500 in this case)
                frame_surface = pygame.transform.scale(frame_surface, (600, 450))
                
                screen.fill(black)
                screen.blit(background, (0, 0))
                screen.blit(frame_surface, (133, 50))  # Center the video on screen

        # Draw buttons
        buttons = [
            (backward_button, '<<'),
            (play_pause_button, 'Pause' if is_playing else 'Play'),
            (forward_button, '>>'),
            (speed_button, 'Speed' if video_speed == 1.0 else 'Normal'),
            (back_button, 'Back')
        ]

        for button_rect, text in buttons:
            draw_button(button_rect, text)

        pygame.display.flip()
        clock.tick(30*video_speed)

# Load functions for different types of images
def round_image(image, corner_radius):
    # Create a mask with rounded corners
    mask = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=corner_radius)

    # Create a new surface with an alpha channel (per-pixel transparency)
    rounded_image = pygame.Surface((image.get_width(), image.get_height()), pygame.SRCALPHA)
    rounded_image.blit(image, (0, 0))
    rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return rounded_image

# Update the load_number_images function to use the updated round_image function
def load_number_images(level):
    """
    Load number images for the given level.
    """
    alphabet_images.clear()
    compare_images.clear()
    
    if level >= 8:
        for i in range(0, 101):  # Adjusted for numbers 0 to 100
            image_path = os.path.join(main_number_folder, f'{i}.png')
            
            if os.path.exists(image_path):
                image = pygame.image.load(image_path)
                image = pygame.transform.smoothscale(image, image_size)
                image = round_image(image, 20)  # Apply slight rounding
                alphabet_images[i] = image
                compare_images[i] = image
            else:
                print(f'Image for number {i} not found. Make sure {image_path} exists.')
    else:
        print(f'Invalid level {level} for number images.')

def load_symbol_images(level):
    alphabet_images.clear()
    compare_images.clear()
    folder_index = level - 1
    if 0 <= folder_index < len(symbol_folders):
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), symbol_folders[folder_index])
        for i in range(1, 33):  # Adjusted for symbols 1 to 32
            main_image_path = os.path.join(main_symbol_folder, f'{i}.png')
            compare_image_path = os.path.join(image_folder, f'{i}.png')

            if os.path.exists(main_image_path):
                image = pygame.image.load(main_image_path)
                image = pygame.transform.smoothscale(image, image_size)
                image = round_image(image, 20)  # Apply slight rounding
                alphabet_images[i] = image
            else:
                print(f'Main image for symbol {i} not found. Make sure {main_image_path} exists.')

            if os.path.exists(compare_image_path):
                image = pygame.image.load(compare_image_path)
                image = pygame.transform.smoothscale(image, image_size)
                image = round_image(image, 20)  # Apply slight rounding
                compare_images[i] = image
            else:
                print(f'Compare image for symbol {i} not found. Make sure {compare_image_path} exists.')
    else:
        print(f'Invalid level {level} for symbol images.')

def load_math_number_images(image_size):
    images = {}
    math_img_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_number_images')
    
    for i in range(0, 101):
        image_path = os.path.join(math_img_folder, f'{i}.png')
        
        if os.path.exists(image_path):
            image = pygame.image.load(image_path)
            image = pygame.transform.smoothscale(image, image_size)
            image = round_image(image, 20)  # Apply slight rounding
            images[i] = image
        else:
            print(f'Main image for number {i} not found. Make sure it exists.')    
    return images

def load_math_symbol_images(level):
    """
    Load math symbol images for the given level.
    """
    alphabet_images.clear()
    compare_images.clear()
    
    if level >= 6:
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_math_symbols')
        
        for i in range(1, 23):  # Adjusted for symbols 1 to 22
            image_path = os.path.join(image_folder, f'{i}.png')

            if os.path.exists(image_path):
                image = pygame.image.load(image_path)
                image = pygame.transform.smoothscale(image, image_size)
                image = round_image(image, 20)  # Apply slight rounding
                alphabet_images[i] = image
                compare_images[i] = image
            else:
                print(f'Image for symbol {i} not found. Make sure {image_path} exists.')
    else:
        print(f'Invalid level {level} for math symbol images.')

def load_alphabet_images(level):
    alphabet_images.clear()
    compare_images.clear()
    folder_index = level - 15
    if 0 <= folder_index < len(font_folders):
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), font_folders[folder_index])
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            main_image_path = os.path.join(main_image_folder, f'{letter}.png')
            compare_image_path = os.path.join(image_folder, f'{letter.lower()}.png')

            if os.path.exists(main_image_path):
                image = pygame.image.load(main_image_path)
                image = pygame.transform.smoothscale(image, image_size)
                image = round_image(image, 20)  # Apply slight rounding
                alphabet_images[letter] = image
            else:
                print(f'Main image for {letter} not found. Make sure {main_image_path} exists.')

            if os.path.exists(compare_image_path):
                image = pygame.image.load(compare_image_path)
                image = pygame.transform.smoothscale(image, image_size)
                image = round_image(image, 20)  # Apply slight rounding
                compare_images[letter] = image
            else:
                print(f'Compare image for {letter} not found. Make sure {compare_image_path} exists.')
    else:
        print(f'Invalid level {level} for alphabet images.')

def load_hindi_alphabet_images(level):
    alphabet_images.clear()
    compare_images.clear()
    
    if 22 <= level < 26:
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main_word_images')
    elif 26 <= level < 29:
        image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images_26')
    else:
        print(f'Invalid level {level} for word images.')
        return

    for i in range(1, 50):
        main_image_path = os.path.join(main_word_folder, f'{i}.png')
        compare_image_path = os.path.join(image_folder, f'{i}.png')

        if os.path.exists(main_image_path):
            image = pygame.image.load(main_image_path)
            image = pygame.transform.smoothscale(image, image_size)
            image = round_image(image, 20)  # Apply slight rounding
            alphabet_images[i] = image
        else:
            print(f'Main image for word {i} not found. Make sure {main_image_path} exists.')

        if os.path.exists(compare_image_path):
            image = pygame.image.load(compare_image_path)
            image = pygame.transform.smoothscale(image, image_size)
            image = round_image(image, 20)  # Apply slight rounding
            compare_images[i] = image
        else:
            print(f'Compare image for word {i} not found. Make sure {compare_image_path} exists.')


# Load and set the window icon
icon_path = os.path.join(main_image_folder, 'A.png')
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
else:
    print(f"Icon image file not found: {icon_path}")

# Load background image
background_path = os.path.join(main_image_folder, 'bg1.png')
if os.path.exists(background_path):
    background = pygame.image.load(background_path)
    background = pygame.transform.smoothscale(background, (screen_width, screen_height))
else:
    print(f"Background image file not found: {background_path}")

# Load sounds
correct_sound_path = os.path.join(main_image_folder, 'correct.wav')
wrong_sound_path = os.path.join(main_image_folder, 'wrong.wav')
background_music_path = os.path.join(main_image_folder, 'background_music.mp3')
win_sound_path = os.path.join(main_image_folder, 'win.wav')

if os.path.exists(correct_sound_path):
    correct_sound = pygame.mixer.Sound(correct_sound_path)
else:
    print(f"Correct sound file not found: {correct_sound_path}")

if os.path.exists(wrong_sound_path):
    wrong_sound = pygame.mixer.Sound(wrong_sound_path)
else:
    print(f"Wrong sound file not found: {wrong_sound_path}")

if os.path.exists(win_sound_path):
    win_sound = pygame.mixer.Sound(win_sound_path)
else:
    print(f"Win sound file not found: {win_sound_path}")

# Check if the background music file exists
if os.path.exists(background_music_path):
    # Load and play the background music
    pygame.mixer.music.load(background_music_path)
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
else:
    print(f"Background music file not found: {background_music_path}")

# Initialize volume variables for different categories
background_volume = 0.5
correct_volume = 0.5
wrong_volume = 0.5
win_volume = 0.5
# Set initial volumes
pygame.mixer.music.set_volume(background_volume)
correct_sound.set_volume(correct_volume)
wrong_sound.set_volume(wrong_volume)
win_sound.set_volume(win_volume)

#fonts
font_ss = pygame.font.SysFont("Arial", 20)
font_small = pygame.font.SysFont("Arial", 30)
font_sm = pygame.font.SysFont("Arial", 35)
font_medium = pygame.font.SysFont("Arial", 45)
font_large = pygame.font.SysFont("Arial", 70)
font_ll=pygame.font.SysFont("Arial", 80)
FONT1=font_large
FONT2 = font_medium

# Encouraging sentences for winning
encouraging_sentences_win = [
    "Great job!", "You did it!", "Fantastic!", "You're amazing!", "Keep it up!", "Well done!", "Excellent!", "Bravo!",
    "Wonderful!", "You're the best!", "Superb!", "Impressive!", "Outstanding!", "Incredible!", "Terrific!", "Remarkable!",
    "Spectacular!", "You're unstoppable!", "Marvelous!", "Exceptional!", "Unbelievable!", "Astounding!", "Magnificent!",
    "Superstar!", "You're on fire!", "You're a genius!", "Amazing effort!", "Great work, keep it up!", "You nailed it!",
    "Superb effort!", "You're doing great!", "You're a champion!", "Way to go!", "Outstanding!", "You're brilliant!",
    "Top-notch effort!", "You're a winner!", "Incredible performance!", "Fantastic job!", "Simply outstanding!",
    "You're a superstar!", "You're unstoppable!", "Absolutely fantastic!", "Keep shining!", "Remarkable effort!",
    "Exceptional work!", "Brilliant performance!", "You're a rockstar!", "Phenomenal!", "You're on a winning streak!",
    "You're a legend!", "Unstoppable greatness!"
]

# Encouraging sentences for pause
encouraging_sentences_pause = [
    "You're the best!", "Don't give up!", "You're doing great!", "Keep pushing!", "Stay focused!", "You can do it!",
    "Almost there!", "Keep trying!", "Stay positive!", "Believe in yourself!", "Never give up!", "Take a breather!",
    "Great job so far!", "You're a star!", "You are doing great!", "Stay strong!", "You're unstoppable!", "Keep it up!",
    "You've got this!", "Stay motivated!", "Keep believing!", "One step at a time!", "Stay resilient!", "You're amazing!",
    "Keep going!", "You're a champion!", "You're a winner!", "You're on the right track!", "You're making great progress!",
    "Push yourself!", "Keep the faith!", "Stay determined!", "Believe and achieve!"
]

# Encouraging sentences for level transition
encouraging_sentences_transition = [
    "Level up!", "On to the next challenge!", "You're doing amazing!", "Keep it up!", "Fantastic progress!",
    "Keep pushing forward!", "You're unstoppable!", "Amazing work!", "Get ready for the next level!", "You're on fire!",
    "Keep going!", "You're a pro!", "Next level, here you come!", "Impressive work!", "You're on a roll!", "Keep the momentum!",
    "Outstanding effort!", "Next level awaits!", "You're a champion!", "Unbelievable progress!", "Epic performance!",
    "Level complete!", "Well done!", "You're smashing it!", "Incredible journey!", "Awesome job!", "Rising star!",
    "You're a force to be reckoned with!", "Level mastered!", "Perseverance pays off!", "You're on top of your game!",
    "You're a winner!", "One level closer!", "You're reaching new heights!", "Champion mentality!"
]
# Initialize high scores dictionary
high_scores = []
# Game start time
start_time = 0
def add_high_score(score):
    print("Before adding new score:", high_scores)
    high_scores.append(score)  # Append the new score
    high_scores.sort()  # Sort in ascending order
    if len(high_scores) > 5:  # Keep only the top 5 scores
        high_scores.pop(-1)  # Remove the highest score (last element)
    print("After adding new score:", high_scores)

# Function to draw button
def draw_button(button_rect, text):
    global dark_mode
    if dark_mode:
        bg_color = black
        hover_color = (100, 100, 100)
        text_color = white
        border_color = white
    else:
        bg_color = BUTTON_COLOR
        hover_color = BUTTON_HOVER_COLOR
        text_color = white
        border_color = white
        if (text=="Back" or text=="Quit"):
            bg_color =red
            hover_color =blue
            text_color = white

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, border_color, button_rect, width=3, border_radius=10)
    render_centered_text_wob(text, font_small, text_color, button_rect.centerx, button_rect.centery)
#without border
def render_text_wob(text, x, y, font, color):
    global dark_mode
    text_surface = font.render(text, True, white)
    screen.blit(text_surface, (x, y))
#without border
def render_centered_text_wob(text, font, color, center_x, center_y):
    global dark_mode
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

# Updated draw_text_with_border function
def draw_text_with_border(surface, text, font, text_color, border_color, pos):
    text_surface = font.render(text, True, text_color)
    border_surface = font.render(text, True, border_color)
    
    x, y = pos
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        surface.blit(border_surface, (x + dx, y + dy))
    
    text_rect = text_surface.get_rect(topleft=pos)
    surface.blit(text_surface, text_rect)

# with border
def render_text(text, x, y, font, color):
    global dark_mode
    border_color =  black
    draw_text_with_border(screen, text, font, color, border_color, (x, y))

#with border
def render_centered_text(text, font, color, center_x, center_y):
    global dark_mode
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    
    border_color =  black
    draw_text_with_border(screen, text, font, color, border_color, text_rect.topleft)

# Function to draw progress bar
def draw_progress_bar(x, y, width, height, value, max_value, label):
    global dark_mode
    # Colors based on dark mode
    bg_color = dark_gray if dark_mode else gray
    fg_color = lime if dark_mode else lime
    border_color = white
    text_color = white

    # Draw the background with rounded corners
    pygame.draw.rect(screen, bg_color, (x, y, width+20, height), border_radius=10)

    # Draw the filled part with a gradient
    fill_width = (value / max_value) * width if max_value != 0 else 0
    for i in range(int(fill_width)):
        pygame.draw.rect(screen, lime, (x, y, fill_width, height), border_radius=10)
    # Draw the border with rounded corners
    pygame.draw.rect(screen, border_color, (x, y, width+20, height), 3, border_radius=10)

    # Render the label and value text
    render_text(f'{label}: {value:.2f}/ {max_value:.2f}', x + 5, y + 25, font_ss, white)

# Function to pause screen
def pause_screen(high_score):
    paused = True
    current_sentence = random.choice(encouraging_sentences_pause)
    global start_time
    pause_start = time.time()  # Record the time when paused

    while paused:
        screen.fill(white)
        screen.blit(background, (0, 0))

        render_centered_text('Game Paused', FONT1, white, screen_width // 2, screen_height // 2 - 250)
        render_centered_text(current_sentence, FONT1, white, screen_width // 2, screen_height // 2 - 150)
        render_centered_text(f'High Score: {high_score:.2f}s', FONT2, white, screen_width // 2, screen_height // 2 - 50)

        resume_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50 + 50, 200, 50)
        dashboard_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20 + 50, 200, 50)
        settings_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 90 + 50, 200, 50)
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 160 + 50, 200, 50)

        buttons = [
            (resume_button, 'Resume'),
            (dashboard_button, 'Dashboard'),
            (settings_button, 'Settings'),
            (quit_button, 'Quit'),
        ]

        for button_rect, text in buttons:
            draw_button(button_rect, text)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(event.pos):
                    pause_end = time.time()  # Record the time when resumed
                    pause_duration = pause_end - pause_start
                    start_time += pause_duration  # Adjust the start_time by adding the paused duration
                    paused = False
                elif dashboard_button.collidepoint(event.pos):
                    dashboard_screen()
                    start_time = time.time()  # Reset start time after viewing the dashboard
                elif settings_button.collidepoint(event.pos):
                    settings()
                    start_time = time.time()  # Reset start time after settings
                elif quit_button.collidepoint(event.pos):
                    start()

# Function to display the level transition screen
def level_transition_screen(level, high_score):
    transition_screen = True
    current_sentence = random.choice(encouraging_sentences_transition)

    add_high_score(high_score)  # Add high score once before the loop

    global start_time
    start_time = 0.0

    # Map the actual level to the visual level (1-7)
    visual_level = (level - 1) % 7 + 1

    while transition_screen:
        screen.fill(white)
        screen.blit(background, (0, 0))

        if level == 7:
            render_centered_text(f'Part 1 Completed!', FONT1, white, screen_width // 2, screen_height // 2 - 250)
        elif level == 14:
            render_centered_text(f'Part 2 Completed!', FONT1, white, screen_width // 2, screen_height // 2 - 250)
        elif level == 21:
            render_centered_text(f'Part 3 Completed!', FONT1, white, screen_width // 2, screen_height // 2 - 250)
        else:
            render_centered_text(f'Level {visual_level} Complete!', FONT1, white, screen_width // 2, screen_height // 2 - 250)

        render_centered_text(current_sentence, FONT1, white, screen_width // 2, screen_height // 2 - 150)
        render_centered_text(f'High Score: {high_score:.2f}s', FONT2, white, screen_width // 2, screen_height // 2 - 50)

        dashboard_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 70, 200, 50)
        continue_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 145, 200, 50)
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 220, 200, 50)

        buttons = [
            (continue_button, 'Continue'),
            (dashboard_button, 'Dashboard'),
            (quit_button, 'Quit')
        ]

        for button_rect, text in buttons:
            draw_button(button_rect, text)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    transition_screen = False
                    return
                elif dashboard_button.collidepoint(event.pos):
                    dashboard_screen()
                    start_time = time.time()  # Reset start time after viewing the dashboard
                elif quit_button.collidepoint(event.pos):
                    start()

# Function to display the win screen
def win_screen(high_score):
    pygame.mixer.music.stop()
    if 'win_sound' in globals():
        win_sound.play()
    current_sentence = random.choice(encouraging_sentences_win)

    add_high_score(high_score)  # Add high score once before the loop

    global start_time
    screen_start_time = start_time  # Record the time when win screen starts

    while True:
        screen.fill(white)
        screen.blit(background, (0, 0))
        render_centered_text("YOU WON!!!", FONT1, white, screen_width // 2, screen_height // 2 - 180)
        render_centered_text(current_sentence, FONT1, white, screen_width // 2, screen_height // 2 - 120)
        render_centered_text(f'High Score: {high_score:.2f}s', FONT2, white, screen_width // 2, screen_height // 2 - 50)

        play_again_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 30, 200, 50)
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 130, 200, 50)
        dashboard_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 230, 200, 50)

        buttons = [
            (play_again_button, 'Play Again'),
            (dashboard_button, 'Dashboard'),
            (quit_button, 'Quit')
        ]

        for button_rect, text in buttons:
            draw_button(button_rect, text)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
                # pygame.quit()
                # exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    pygame.mixer.music.play(-1)
                    return True
                elif dashboard_button.collidepoint(event.pos):
                    dashboard_screen()
                    start_time = screen_start_time  # Reset start time after viewing the dashboard
                elif quit_button.collidepoint(event.pos):
                    start()
        # Update elapsed time
        start_time = screen_start_time + (time.time() - screen_start_time)

# Function to display the dashboard
def dashboard_screen():
    global high_scores  # Access the global high_scores list
    dashboard_open = True
    current_sentence = random.choice(encouraging_sentences_win)
    
    global start_time
    screen_start_time = start_time  # Record the time when dashboard screen starts
    
    while dashboard_open:
        screen.fill(white)
        screen.blit(background, (0, 0))
        
        render_centered_text('Dashboard', font_large, white, screen_width // 2, screen_height // 2 - 260)
        render_centered_text(current_sentence, FONT1, white, screen_width // 2, screen_height // 2 - 190)
        render_centered_text('High Scores', font_medium, white, screen_width // 2 - 100, screen_height // 2 - 130)
        
        # Display high scores for each level
        for level in range(5):
            if level < len(high_scores):
                render_centered_text(f'{level+1}.  {high_scores[level]:.2f}s', font_medium, white, screen_width // 2 - 100, 235 + level * 50)
            else:
                render_centered_text(f'{level+1}.  --', font_medium, white, screen_width // 2 - 100, 235 + level * 50)

        back_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 170, 200, 50)
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 240, 200, 50)

        # Draw buttons
        draw_button(back_button, 'Back')
        draw_button(quit_button, 'Quit')
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    dashboard_open = False
                elif quit_button.collidepoint(event.pos):
                    start()
        # Update elapsed time
        start_time = screen_start_time + (time.time() - screen_start_time)

# Function to select level
def select_level():
    running = True
    selected_level = None  # Initialize as None to avoid premature selection

    while running:
        screen.fill(white)
        screen.blit(background, (0, 0))

        render_centered_text('Select Level', font_large, white, screen_width // 2, 50)

        level_buttons = []
        button_width = 80
        button_height = 35
        levels_per_column = 7
        button_y_start = 170
        headings = ["Symbols", "Maths", "English", "Hindi"]

        for column in range(4):
            heading_x = 100 + column * 200
            render_centered_text(headings[column], font_medium, white, heading_x + button_width // 2, button_y_start - 40)
            button_y = button_y_start
            for row in range(levels_per_column):
                visible_level = row + 1
                actual_level = column * levels_per_column + row + 1
                button_rect = pygame.Rect(heading_x, button_y, button_width, button_height)
                level_buttons.append((actual_level, button_rect))
                draw_button(button_rect, f'{visible_level}')
                button_y += 50  # Adjust spacing between buttons

        back_button_rect = pygame.Rect(screen_width // 2 - 75, screen_height - 60, 150, 45)
        draw_button(back_button_rect, 'Back')
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for actual_level, button_rect in level_buttons:
                    if button_rect.collidepoint(event.pos):
                        selected_level = actual_level
                        running = False
                        break
                if back_button_rect.collidepoint(event.pos):
                    running = False
                    break

    return selected_level

def game1(start_level):
    global high_score, dark_mode, difficulty

    running = True
    current_symbol = random.choice(range(1, 33))
    choices = []
    start_time = time.time()
    score = 0
    high_score = 0.0
    level = start_level
    guessed_symbols = set()
    show_wrong = False
    wrong_time = 0
    correct_time=0
    choice_colors = [None] * 5  # To store the colors of the choice buttons
    correct_chosen = False  # Flag to check if the correct option was chosen
    show_correct=False
    choice_rects = []


    load_symbol_images(level)

    pause_button = pygame.Rect(screen_width - 150, 10, 143, 45)
    dashboard_button = pygame.Rect(screen_width - 150, 70, 143, 45)
    settings_button = pygame.Rect(screen_width - 150, 130, 143, 45)
    quit_button = pygame.Rect(screen_width - 150, 190, 143, 45)

    while running:
        if difficulty == 'Easy':
            num_choices = 3
        elif difficulty == 'Medium':
            num_choices = 4
        elif difficulty == 'Hard':
            num_choices = 5

        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pause_button.collidepoint(mouse_pos):
                    pause_screen(high_score)
                    start_time = time.time()
                elif quit_button.collidepoint(mouse_pos):
                    return
                elif dashboard_button.collidepoint(mouse_pos):
                    dashboard_screen()
                    start_time = time.time()
                elif settings_button.collidepoint(event.pos):
                    prev_difficulty = difficulty
                    settings_wd()
                    start_time = time.time()
                    if prev_difficulty != difficulty:
                        load_symbol_images(level)
                        choices = []  # Reset choices if difficulty changed
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        if choices[i] == current_symbol:
                            choice_colors[i] = green
                            correct_chosen = True
                            if 'correct_sound' in globals():
                                correct_sound.play()
                            show_correct = True
                            correct_time = time.time()  
                        else:
                            choice_colors[i] = red
                            if 'wrong_sound' in globals():
                                wrong_sound.play()
                            show_wrong = True
                            wrong_time = time.time()
                        break
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        choice_colors[i] = purple
                    else:
                        choice_colors[i] = None

        render_text('Current Symbol: ', 50, 50, font_medium, snow if dark_mode else white)

        if current_symbol in alphabet_images:
            screen.blit(alphabet_images[current_symbol], (330, 25))

        if not choices:
            choices = [current_symbol]
            while len(choices) < num_choices:
                rand_symbol = random.choice(range(1, 33))
                if rand_symbol not in choices:
                    choices.append(rand_symbol)
            random.shuffle(choices)

        choice_rects = []
        total_padding = 50
        image_width = 100
        total_image_width = num_choices * image_width
        available_width = screen_width - total_padding - total_image_width
        spacing = (available_width // (num_choices + 1))

        for i, choice in enumerate(choices):
            x = total_padding // 2 + spacing * (i + 1) + image_width * i
            y = 450
            choice_rect = pygame.Rect(x - 10, y - 10, image_width + 20, 120)  # Increased hover area
            choice_rects.append(choice_rect)
            if choice_colors[i]:
                pygame.draw.rect(screen, choice_colors[i], choice_rect, border_radius=15)  # Add rounded corners
            if choice in compare_images:
                rounded_image = round_image(compare_images[choice], 15)
                screen.blit(rounded_image, (x, y))
            else:
                print(f'Missing image for symbol {choice} in folder {level}')

        render_text(f'High Score: {high_score:.2f}s', 50, 150-10, font_sm, snow if dark_mode else white)
        render_text(f'Current Score: {score:.2f}s', 50-10, 225, font_sm, snow if dark_mode else white)

        draw_progress_bar(50, 325, screen_width - 100, 20, level, 7, "Level Progress")

        if show_wrong:
            render_text('Wrong', screen_width // 2 - 65, 260, font_medium, red)
            if time.time() - wrong_time > 1:
                show_wrong = False
        if show_correct:
            render_text('Correct', screen_width // 2 - 65, 260, font_medium, green)
            if time.time() - correct_time > .0125:
                show_correct  = False

        draw_button(pause_button, 'Pause')
        draw_button(quit_button, 'Quit')
        draw_button(dashboard_button, 'Dashboard')
        draw_button(settings_button, 'Settings')
        pygame.display.flip()

        if correct_chosen:
            # pygame.time.wait(250)  # Wait for 1/4th of a second
            current_symbol = random.choice(range(1, 31))
            choices = []
            choice_colors = [None] * 5  # Reset colors for new choices
            score = time.time() - start_time
            if high_score == 0.0 or score < high_score:
                high_score = score
            start_time = time.time()
            show_wrong = False
            guessed_symbols.add(current_symbol)
            if len(guessed_symbols) == 15:
                if level < 5:
                    level_transition_screen(level, high_score)
                    level += 1
                    start_time = time.time()
                    guessed_symbols.clear()
                    load_symbol_images(level)
                else:
                    level_transition_screen(level, high_score)
                    level += 1
                    game2(level)
                    start()
            correct_chosen = False  # Reset flag after processing

    pygame.quit()

def game2(start_level):
    global high_score, dark_mode, difficulty

    running = True
    current_number = random.choice(range(1, 23))
    choices = []
    start_time = time.time()
    score = 0
    high_score = 0.0
    level = start_level
    guessed_numbers = set()
    show_wrong = False
    wrong_time = 0
    correct_time=0
    choice_colors = [None] * 5  # To store the colors of the choice buttons
    correct_chosen = False  # Flag to check if the correct option was chosen
    show_correct=False
    choice_rects = []

    load_math_symbol_images(level)

    pause_button = pygame.Rect(screen_width - 150, 10, 143, 45)
    dashboard_button = pygame.Rect(screen_width - 150, 70, 143, 45)
    settings_button = pygame.Rect(screen_width - 150, 130, 143, 45)
    quit_button = pygame.Rect(screen_width - 150, 190, 143, 45)

    while running:
        if difficulty == 'Easy':
            num_choices = 3
        elif difficulty == 'Medium':
            num_choices = 4
        elif difficulty == 'Hard':
            num_choices = 5

        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pause_button.collidepoint(mouse_pos):
                    pause_screen(high_score)
                    start_time = time.time()
                elif quit_button.collidepoint(mouse_pos):
                    return
                elif dashboard_button.collidepoint(mouse_pos):
                    dashboard_screen()
                    start_time = time.time()
                elif settings_button.collidepoint(event.pos):
                    prev_difficulty = difficulty
                    settings_wd()
                    start_time = time.time()
                    if prev_difficulty != difficulty:
                        load_number_images(level)
                        choices = []  # Reset choices if difficulty changed
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        if choices[i] == current_number:
                            choice_colors[i] = green
                            correct_chosen = True
                            if 'correct_sound' in globals():
                                correct_sound.play()
                            show_correct = True
                            correct_time = time.time()    
                        else:
                            choice_colors[i] = red
                            if 'wrong_sound' in globals():
                                wrong_sound.play()
                            show_wrong = True
                            wrong_time = time.time()
                        break
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        choice_colors[i] = purple
                    else:
                        choice_colors[i] = None

        render_text('Current Symbol:  ', 50, 50, font_medium, snow if dark_mode else white)

        if current_number in alphabet_images:
            screen.blit(alphabet_images[current_number], (335, 25))

        if not choices:
            choices = [current_number]
            while len(choices) < num_choices:
                rand_number = random.choice(range(1, 23))
                if rand_number not in choices:
                    choices.append(rand_number)
            random.shuffle(choices)

        choice_rects = []
        total_padding = 50
        image_width = 100
        total_image_width = num_choices * image_width
        available_width = screen_width - total_padding - total_image_width
        spacing = (available_width // (num_choices + 1))

        for i, choice in enumerate(choices):
            x = total_padding // 2 + spacing * (i + 1) + image_width * i
            y = 450
            choice_rect = pygame.Rect(x - 10, y - 10, image_width + 20, 120)  # Increased hover area
            choice_rects.append(choice_rect)
            if choice_colors[i]:
                pygame.draw.rect(screen, choice_colors[i], choice_rect, border_radius=15)  # Add rounded corners
            if choice in alphabet_images:
                rounded_image = round_image(alphabet_images[choice], 15)
                screen.blit(rounded_image, (x, y))
            else:
                print(f'Missing image for number {choice} in folder {level}')

        render_text(f'High Score: {high_score:.2f}s', 50, 150-10, font_sm, snow if dark_mode else white)
        render_text(f'Current Score: {score:.2f}s', 50-10, 225, font_sm, snow if dark_mode else white)

        draw_progress_bar(50, 325, screen_width - 100, 20, level, 7, "Level Progress")

        if show_wrong:
            render_text('Wrong', screen_width // 2 - 65, 260, font_medium, red)
            if time.time() - wrong_time > 1:
                show_wrong = False
        if show_correct:
            render_text('Correct', screen_width // 2 - 65, 260, font_medium, green)
            if time.time() - correct_time > .0125:
                show_correct  = False

        draw_button(pause_button, 'Pause')
        draw_button(quit_button, 'Quit')
        draw_button(dashboard_button, 'Dashboard')
        draw_button(settings_button, 'Settings')
        pygame.display.flip()

        if correct_chosen:
            # pygame.time.wait(250)  # Wait for 1/4th of a second
            current_number = random.choice(range(1, 23))
            choices = []
            choice_colors = [None] * 5  # Reset colors for new choices
            score = time.time() - start_time
            if high_score == 0.0 or score < high_score:
                high_score = score
            start_time = time.time()
            show_wrong = False
            guessed_numbers.add(current_number)
            if len(guessed_numbers) == 15:
                if level < 5:
                    level_transition_screen(level, high_score)
                    level += 1
                    start_time = time.time()
                    guessed_numbers.clear()
                    load_number_images(level)
                else:
                    level_transition_screen(level, high_score)
                    level += 1
                    game3(level)
                    start()
            correct_chosen = False  # Reset flag after processing

    pygame.quit()

def game3(start_level):
    global high_score, dark_mode, difficulty

    running = True
    current_number = random.choice(range(0,100))
    choices = []
    start_time = time.time()
    score = 0
    high_score = 0.0
    level = start_level
    guessed_numbers = set()
    show_wrong = False
    wrong_time = 0
    correct_time=0
    choice_colors = [None] * 5  # To store the colors of the choice buttons
    correct_chosen = False  # Flag to check if the correct option was chosen
    show_correct=False
    choice_rects = []

    load_number_images(level)

    pause_button = pygame.Rect(screen_width - 150, 10, 143, 45)
    dashboard_button = pygame.Rect(screen_width - 150, 70, 143, 45)
    settings_button = pygame.Rect(screen_width - 150, 130, 143, 45)
    quit_button = pygame.Rect(screen_width - 150, 190, 143, 45)

    while running:
        if difficulty == 'Easy':
            num_choices = 3
        elif difficulty == 'Medium':
            num_choices = 4
        elif difficulty == 'Hard':
            num_choices = 5

        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pause_button.collidepoint(mouse_pos):
                    pause_screen(high_score)
                    start_time = time.time()
                elif quit_button.collidepoint(mouse_pos):
                    return
                elif dashboard_button.collidepoint(mouse_pos):
                    dashboard_screen()
                    start_time = time.time()
                elif settings_button.collidepoint(event.pos):
                    prev_difficulty = difficulty
                    settings_wd()
                    start_time = time.time()
                    if prev_difficulty != difficulty:
                        load_number_images(level)
                        choices = []  # Reset choices if difficulty changed
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        if choices[i] == current_number:
                            choice_colors[i] = green
                            correct_chosen = True
                            if 'correct_sound' in globals():
                                correct_sound.play()
                            show_correct=True
                            correct_time=time.time()    
                        else:
                            choice_colors[i] = red
                            if 'wrong_sound' in globals():
                                wrong_sound.play()
                            show_wrong = True
                            wrong_time = time.time()
                        break
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        choice_colors[i] = purple
                    else:
                        choice_colors[i] = None

        render_text('Current Number: ', 50, 50, font_medium, snow if dark_mode else white)

        if current_number in alphabet_images:
            screen.blit(alphabet_images[current_number], (335, 25))

        if not choices:
            choices = [current_number]
            while len(choices) < num_choices:
                rand_number = random.choice(range(1, 38))
                if rand_number not in choices:
                    choices.append(rand_number)
            random.shuffle(choices)

        choice_rects = []
        total_padding = 50
        image_width = 100
        total_image_width = num_choices * image_width
        available_width = screen_width - total_padding - total_image_width
        spacing = (available_width // (num_choices + 1))

        for i, choice in enumerate(choices):
            x = total_padding // 2 + spacing * (i + 1) + image_width * i
            y = 450
            choice_rect = pygame.Rect(x - 10, y - 10, image_width + 20, 120)  # Increased hover area
            choice_rects.append(choice_rect)
            if choice_colors[i]:
                pygame.draw.rect(screen, choice_colors[i], choice_rect, border_radius=15)  # Add rounded corners
            if choice in compare_images:
                rounded_image = round_image(compare_images[choice], 15)
                screen.blit(rounded_image, (x, y))
            else:
                print(f'Missing image for symbol {choice} in folder {level}')

        render_text(f'High Score: {high_score:.2f}s', 50-10, 150, font_sm, snow if dark_mode else white)
        render_text(f'Current Score: {score:.2f}s', 50-10, 225, font_sm, snow if dark_mode else white)

        draw_progress_bar(50, 325, screen_width - 100, 20, level - 7, 7, "Level Progress")

        if show_wrong:
            render_text('Wrong', screen_width // 2 - 65, 260, font_medium, red)
            if time.time() - wrong_time > 1:
                show_wrong = False
        if show_correct:
            render_text('Correct', screen_width // 2 - 65, 260, font_medium, green)
            if time.time() - correct_time > 0.0125:
                show_correct  = False

        draw_button(pause_button, 'Pause')
        draw_button(quit_button, 'Quit')
        draw_button(dashboard_button, 'Dashboard')
        draw_button(settings_button, 'Settings')
        pygame.display.flip()

        if correct_chosen:
            # pygame.time.wait(250)  # Wait for 1/4th of a second
            current_number = random.choice(range(1,101))
            choices = []
            choice_colors = [None] * 5  # Reset colors for new choices
            score = time.time() - start_time
            if high_score == 0.0 or score < high_score:
                high_score = score
            start_time = time.time()
            show_wrong = False
            guessed_numbers.add(current_number)
            if len(guessed_numbers) == 15:
                if level < 10:
                    level_transition_screen(level, high_score)
                    level += 1
                    start_time = time.time()
                    guessed_numbers.clear()
                    load_number_images(level)
                else:
                    level_transition_screen(level, high_score)
                    level += 1
                    game4(level)
                    start()
            correct_chosen = False  # Reset flag after processing

    pygame.quit()

def game4(start_level):
    global high_score, dark_mode, difficulty
    correct_time=0
    running = True
    score = 0
    high_score = 0.0
    level = start_level
    start_time = time.time()
    correct_answers = 0
    show_wrong = False
    wrong_time = 0
    current_question = None
    choice_colors = [None] * 5  # To store the colors of the choice buttons
    correct_chosen = False  # Flag to check if the correct option was chosen
    show_correct=False
    choice_rects = []

    pause_button = pygame.Rect(screen_width - 150, 10, 143, 45)
    dashboard_button = pygame.Rect(screen_width - 150, 70, 143, 45)
    settings_button = pygame.Rect(screen_width - 150, 130, 143, 45)
    quit_button = pygame.Rect(screen_width - 150, 190, 143, 45)

    image_size = (100,100)
    math_images = load_math_number_images(image_size)

    def generate_numbers_and_answer(level):
        while True:
            num1 = random.randint(1, 50)
            num2 = random.randint(1, 50)

            if level == 11:
                correct_answer = num1 + num2
                operator = '+'
            elif level == 12:
                if num1 < num2:
                    num1, num2 = num2, num1
                correct_answer = num1 - num2
                operator = '-'
            elif level == 13:
                correct_answer = num1 * num2
                operator = '*'
            elif level == 14:
                if num2 == 0:
                    continue  # Retry if num2 is zero to avoid division by zero
                if num1 % num2 != 0:
                    continue  # Retry if the division does not result in a whole number
                correct_answer = num1 // num2
                operator = '//'
            else:
                continue
                                  
            if 0 < correct_answer <= 100:
                break

        return num1, num2, operator, correct_answer

    while running:
        if current_question is None:
            current_question = generate_numbers_and_answer(level)
            num1, num2, operator, correct_answer = current_question
            answers = [correct_answer]

            if difficulty == 'Easy':
                num_choices = 3
            elif difficulty == 'Medium':
                num_choices = 4
            elif difficulty == 'Hard':
                num_choices = 5

            while len(answers) < num_choices:
                fake_answer = random.randint(0, 100)
                if fake_answer not in answers:
                    answers.append(fake_answer)
            random.shuffle(answers)

        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pause_button.collidepoint(mouse_pos):
                    pause_screen(high_score)
                    start_time = time.time()
                elif quit_button.collidepoint(mouse_pos):
                    return
                elif dashboard_button.collidepoint(mouse_pos):
                    dashboard_screen()
                    start_time = time.time()
                elif settings_button.collidepoint(event.pos):
                    prev_difficulty = difficulty
                    settings_wd()
                    start_time = time.time()
                    if prev_difficulty != difficulty:
                        answers = []  # Reset choices if difficulty changed
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        if answers[i] == correct_answer:
                            choice_colors[i] = green
                            correct_chosen = True
                            if 'correct_sound' in globals():
                                correct_sound.play()
                            correct_time=time.time()
                            show_correct=True
                            score = time.time() - start_time
                            if high_score == 0.0 or score < high_score:
                                high_score = score
                            start_time = time.time()
                            show_wrong = False
                            correct_answers += 1
                            current_question = None  # Reset question after correct answer
                            if correct_answers >= 15:  # Transition after 15 correct answers
                                if level < 14:
                                    level_transition_screen(level, high_score)
                                    level += 1
                                    correct_answers = 0
                                else:
                                    level_transition_screen(level, high_score)
                                    game5(level + 1)
                                    return
                        else:
                            choice_colors[i] = red
                            if 'wrong_sound' in globals():
                                wrong_sound.play()
                            show_wrong = True
                            wrong_time = time.time()
                        break
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        choice_colors[i] =  purple
                    else:
                        choice_colors[i] = None

        render_text(f'Current Equation: {num1} {operator.replace("//", "/").replace("*", "×")} {num2} = ?', 50, 50, font_medium, snow)

        total_padding = 50
        image_width = 100
        total_image_width = num_choices * image_width
        available_width = screen_width - total_padding - total_image_width
        spacing = available_width // (num_choices + 1)

        choice_rects = []
        for i, answer in enumerate(answers):
            x = total_padding // 2 + spacing * (i + 1) + image_width * i
            y = 450
            choice_rect = pygame.Rect(x - 10, y - 10, image_width + 20, 120)  # Increased hover area
            choice_rects.append(choice_rect)
            if choice_colors[i]:
                pygame.draw.rect(screen, choice_colors[i], choice_rect, border_radius=15)  # Add rounded corners
            if answer in math_images:
                screen.blit(math_images[answer], (x, y))
            else:
                print(f'Missing image for number {answer}')

        render_text(f'High Score: {high_score:.2f}s', 50 - 10, 150, font_sm, snow)
        render_text(f'Current Score: {score:.2f}s', 50 - 10, 225, font_sm, snow)

        draw_progress_bar(50, 325, screen_width - 100, 20, level - 7, 7, "Level Progress")

        if show_wrong:
            render_text('Wrong', screen_width // 2 - 65, 260, font_medium, red)
            if time.time() - wrong_time > .7:
                show_wrong = False
        if show_correct:
            render_text('Correct', screen_width // 2 - 65, 260, font_medium, green)
            if time.time() - correct_time > 0.0125:
                show_correct  = False

        draw_button(pause_button, 'Pause')
        draw_button(quit_button, 'Quit')
        draw_button(dashboard_button, 'Dashboard')
        draw_button(settings_button, 'Settings')
        pygame.display.flip()

        if correct_chosen:
            # pygame.time.wait(700)  # Wait for 3/4th of a second
            correct_chosen = False  # Reset flag after processing

    pygame.quit()

def game5(start_level):
    global high_score, dark_mode, difficulty  # Declare high_score as global so it can be modified

    running = True
    current_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    choices = []
    start_time = time.time()
    score = 0
    high_score = 0.0
    level = start_level  # Start from the selected level
    guessed_letters = set()
    show_wrong = False
    wrong_time = 0
    choice_colors = [None] * 5  # To store the colors of the choice buttons
    correct_chosen = False  # Flag to check if the correct option was chosen
    show_correct=False
    correct_time=0
    choice_rects = []

    load_alphabet_images(level)

    pause_button = pygame.Rect(screen_width - 150, 10, 143, 45)
    dashboard_button = pygame.Rect(screen_width - 150, 70, 143, 45)
    settings_button = pygame.Rect(screen_width - 150, 130, 143, 45)
    quit_button = pygame.Rect(screen_width - 150, 190, 143, 45)

    while running:
        if difficulty == 'Easy':
            num_choices = 3
        elif difficulty == 'Medium':
            num_choices = 4
        elif difficulty == 'Hard':
            num_choices = 5

        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pause_button.collidepoint(mouse_pos):
                    pause_screen(high_score)
                    start_time = time.time()  # Reset start time after pause
                elif quit_button.collidepoint(mouse_pos):
                    return
                elif dashboard_button.collidepoint(mouse_pos):
                    dashboard_screen()
                    start_time = time.time()  # Reset start time after viewing the dashboard
                elif settings_button.collidepoint(event.pos):
                    prev_difficulty = difficulty
                    settings_wd()
                    start_time = time.time()
                    if prev_difficulty != difficulty:
                        load_alphabet_images(level)
                        choices = []  # Reset choices if difficulty changed
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        if choices[i] == current_letter:
                            choice_colors[i] = green
                            correct_chosen = True
                            if 'correct_sound' in globals():
                                correct_sound.play()
                            correct_time=time.time()
                            show_correct=True    
                        else:
                            choice_colors[i] = red
                            if 'wrong_sound' in globals():
                                wrong_sound.play()
                            show_wrong = True
                            wrong_time = time.time()
                        break
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        choice_colors[i] = purple
                    else:
                        choice_colors[i] = None

        render_text('Current Letter: ', 50, 50, font_medium, snow if dark_mode else white)

        if current_letter in alphabet_images:
            screen.blit(alphabet_images[current_letter], (310, 25))

        if not choices:
            choices = [current_letter]
            while len(choices) < num_choices:
                rand_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                if rand_letter not in choices:
                    choices.append(rand_letter)
            random.shuffle(choices)

        choice_rects = []
        total_padding = 50
        image_width = 100
        total_image_width = num_choices * image_width
        available_width = screen_width - total_padding - total_image_width
        spacing = (available_width // (num_choices + 1))

        for i, choice in enumerate(choices):
            x = total_padding // 2 + spacing * (i + 1) + image_width * i
            y = 450
            choice_rect = pygame.Rect(x - 10, y - 10, image_width + 20, 120)  # Increased hover area
            choice_rects.append(choice_rect)
            if choice_colors[i]:
                pygame.draw.rect(screen, choice_colors[i], choice_rect, border_radius=15)  # Add rounded corners
            if choice in compare_images:
                rounded_image = round_image(compare_images[choice], 15)
                screen.blit(rounded_image, (x, y))
            else:
                print(f'Missing image for alphabet {choice} in folder {level}')

        render_text(f'High Score: {high_score:.2f}s', 50-10, 150, font_sm, snow if dark_mode else white)
        render_text(f'Current Score: {score:.2f}s', 50-10, 225, font_sm, snow if dark_mode else white)

        draw_progress_bar(50, 325, screen_width - 100, 20, level - 14, 7, "Level Progress")

        if show_wrong:
            render_text('Wrong', screen_width // 2 - 65, 260, font_medium, red)
            if time.time() - wrong_time > .7:
                show_wrong = False
        if show_correct:
            render_text('Correct', screen_width // 2 - 65, 260, font_medium, green)
            if time.time() - correct_time > 0.0125:
                show_correct  = False

        draw_button(pause_button, 'Pause')
        draw_button(quit_button, 'Quit')
        draw_button(dashboard_button, 'Dashboard')
        draw_button(settings_button, 'Settings')
        pygame.display.flip()

        if correct_chosen:
            # pygame.time.wait(250)  # Wait for 1/4th of a second
            current_letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            choices = []
            choice_colors = [None] * 5  # Reset colors for new choices
            score = time.time() - start_time
            if high_score == 0.0 or score < high_score:
                high_score = score
            start_time = time.time()
            show_wrong = False
            guessed_letters.add(current_letter)
            if len(guessed_letters) == 15:
                if level < 21:
                    level_transition_screen(level, high_score)
                    level += 1
                    start_time = time.time()
                    guessed_letters.clear()
                    load_alphabet_images(level)
                else:
                    level_transition_screen(level, high_score)
                    level += 1
                    game6(level)
                    start()
            correct_chosen = False  # Reset flag after processing

    pygame.quit()

def game6(start_level):
    global high_score, dark_mode, difficulty

    running = True
    current_word = random.choice(range(1, 50))
    choices = []
    start_time = time.time()
    score = 0
    high_score = 0.0
    level = start_level
    guessed_words = set()
    show_wrong = False
    wrong_time = 0
    choice_colors = [None] * 5  # To store the colors of the choice buttons
    correct_chosen = False  # Flag to check if the correct option was chosen
    show_correct=False
    correct_time=0
    choice_rects = []

    load_hindi_alphabet_images(level)

    pause_button = pygame.Rect(screen_width - 150, 10, 143, 45)
    dashboard_button = pygame.Rect(screen_width - 150, 70, 143, 45)
    settings_button = pygame.Rect(screen_width - 150, 130, 143, 45)
    quit_button = pygame.Rect(screen_width - 150, 190, 143, 45)

    while running:
        if difficulty == 'Easy':
            num_choices = 3
        elif difficulty == 'Medium':
            num_choices = 4
        elif difficulty == 'Hard':
            num_choices = 5

        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pause_button.collidepoint(mouse_pos):
                    pause_screen(high_score)
                    start_time = time.time()
                elif quit_button.collidepoint(mouse_pos):
                    return
                elif dashboard_button.collidepoint(mouse_pos):
                    dashboard_screen()
                    start_time = time.time()
                elif settings_button.collidepoint(event.pos):
                    prev_difficulty = difficulty
                    settings_wd()
                    start_time = time.time()
                    if prev_difficulty != difficulty:
                        load_hindi_alphabet_images(level)
                        choices = []  # Reset choices if difficulty changed
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        if choices[i] == current_word:
                            choice_colors[i] = green
                            correct_chosen = True
                            if 'correct_sound' in globals():
                                correct_sound.play()
                            correct_time=time.time() 
                            show_correct=True   
                        else:
                            choice_colors[i] = red
                            if 'wrong_sound' in globals():
                                wrong_sound.play()
                            show_wrong = True
                            wrong_time = time.time()
                        break
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                for i, rect in enumerate(choice_rects):
                    if rect.collidepoint(mouse_pos):
                        choice_colors[i] = purple
                    else:
                        choice_colors[i] = None

        render_text('Current Word: ', 50, 50, font_medium, snow if dark_mode else white)

        if current_word in alphabet_images:
            screen.blit(alphabet_images[current_word], (310, 25))

        if not choices:
            choices = [current_word]
            while len(choices) < num_choices:
                rand_word = random.choice(range(1, 31))
                if rand_word not in choices:
                    choices.append(rand_word)
            random.shuffle(choices)

        choice_rects = []
        total_padding = 50
        image_width = 100
        total_image_width = num_choices * image_width
        available_width = screen_width - total_padding - total_image_width
        spacing = (available_width // (num_choices + 1))

        for i, choice in enumerate(choices):
            x = total_padding // 2 + spacing * (i + 1) + image_width * i
            y = 450
            choice_rect = pygame.Rect(x - 10, y - 10, image_width + 20, 120)  # Increased hover area
            choice_rects.append(choice_rect)
            if choice_colors[i]:
                pygame.draw.rect(screen, choice_colors[i], choice_rect, border_radius=15)  # Add rounded corners
            if choice in compare_images:
                rounded_image = round_image(compare_images[choice], 15)
                screen.blit(rounded_image, (x, y))
            else:
                print(f'Missing image for word {choice} in folder {level}')

        render_text(f'High Score: {high_score:.2f}s', 50, 150-10, font_sm, snow if dark_mode else white)
        render_text(f'Current Score: {score:.2f}s', 50-10, 225, font_sm, snow if dark_mode else white)

        draw_progress_bar(50, 325, screen_width - 100, 20, level-21, 7, "Level Progress")

        if show_wrong:
            render_text('Wrong', screen_width // 2 - 65, 260, font_medium, red)
            if time.time() - wrong_time > .7:
                show_wrong = False
        if show_correct:
            render_text('Correct', screen_width // 2 - 65, 260, font_medium, green)
            if time.time() - correct_time > 0.0125:
                show_correct  = False

        draw_button(pause_button, 'Pause')
        draw_button(quit_button, 'Quit')
        draw_button(dashboard_button, 'Dashboard')
        draw_button(settings_button, 'Settings')
        pygame.display.flip()

        if correct_chosen:
            # pygame.time.wait(250)  # Wait for 1/4th of a second
            current_word = random.choice(range(1, 31))
            choices = []
            choice_colors = [None] * 5  # Reset colors for new choices
            score = time.time() - start_time
            if high_score == 0.0 or score < high_score:
                high_score = score
            start_time = time.time()
            show_wrong = False
            guessed_words.add(current_word)
            if len(guessed_words) == 15:
                if level < 28:
                    level_transition_screen(level, high_score)
                    level += 1
                    start_time = time.time()
                    guessed_words.clear()
                    load_hindi_alphabet_images(level)
                else:
                    win_screen(high_score)
                    start_time = time.time()
                    running = False
            correct_chosen = False  # Reset flag after processing

    pygame.quit()

def draw_button(button_rect, text):
    global dark_mode
    if dark_mode:
        bg_color = black
        hover_color = (100, 100, 100)
        text_color = white
        border_color = white
    else:
        bg_color = BUTTON_COLOR
        hover_color = BUTTON_HOVER_COLOR
        text_color = white
        border_color = white
        if (text=="Back" or text=="Quit"):
            bg_color = red
            hover_color = blue
            text_color = white

    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, border_color, button_rect, width=3, border_radius=10)
    render_centered_text_wob(text, font_small, text_color, button_rect.centerx, button_rect.centery)

def instruction_screen():
    running = True
    while running:
        screen.fill(white)
        screen.blit(background, (0, 0))
        
        render_centered_text('Instructions', font_large, white, screen_width // 2, 50)

        instruction_text = [
            "1. The game consists of various levels.",
            "2. You need to match the related cards.",
            "3. Use the mouse to click on the correct choice.",
            "4. There are different diffuculty levels. ",
            "5. You can pause the game using pause button.",
            "6. Adjust the settings for better experience",
            "7. Get the best score by quickly matching the correct choices."
        ]

        for i, line in enumerate(instruction_text):
            render_text(line, 30, 130 + i * 40, font_sm, white)

        video_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 130, 200, 50)
        back_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 50)

        draw_button(video_button, 'Watch Video')
        draw_button(back_button, 'Back')

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if video_button.collidepoint(event.pos):
                    # Replace 'path/to/your/video.mp4' with the actual path to your video file
                    play_video(video)
                elif back_button.collidepoint(event.pos):
                    return  # Go back to the start screen                

def start():
    running = True
    while running:
        screen.fill(white)
        screen.blit(background, (0, 0))
    
        render_centered_text('Match Mania', font_large, white, screen_width // 2, screen_height // 2 - 220)
        
        instruction_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 100, 200, 50)
        start_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50)
        levels_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
        settings_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 125, 200, 50)
        quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 50)

        draw_button(instruction_button, 'Instructions')
        draw_button(start_button, 'Start Game')
        draw_button(levels_button, 'Levels')
        draw_button(settings_button, 'Settings')
        draw_button(quit_button, 'Quit')

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Ensure the script exits
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if instruction_button.collidepoint(event.pos):
                    instruction_screen()
                elif start_button.collidepoint(event.pos):
                    game1(start_level=1)  # Start from level 1
                elif levels_button.collidepoint(event.pos):
                    selected_level = select_level()
                    if selected_level is not None:
                        if selected_level >= 1 and selected_level <= 5:
                            game1(selected_level)
                        elif selected_level >= 6 and selected_level <= 7:
                            game2(selected_level)
                        elif selected_level >= 8 and selected_level <= 10:
                            game3(selected_level)
                        elif selected_level >= 11 and selected_level <= 14:
                            game4(selected_level)
                        elif selected_level >= 15 and selected_level <= 21:
                            game5(selected_level)
                        elif selected_level >= 22 and selected_level <= 28:
                            game6(selected_level)
                elif settings_button.collidepoint(event.pos):
                    settings()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Ensure the script exits

#to change backgroung
def change_theme():
    global background_path, background

    themes = [
        os.path.join(main_image_folder, 'bg1.png'),
        os.path.join(main_image_folder, 'bg2.png'),
        os.path.join(main_image_folder, 'bg3.png'),
        os.path.join(main_image_folder, 'bg4.png'),
        os.path.join(main_image_folder, 'bg5.png'),
        os.path.join(main_image_folder, 'bg6.png'),
        os.path.join(main_image_folder, 'bg7.png'),
        os.path.join(main_image_folder, 'bg8.png')
    ]
    
    theme_index = 0
    choosing_theme = True

    while choosing_theme:
        screen.fill(white)
        current_theme_path = themes[theme_index]
        current_theme = pygame.image.load(current_theme_path)
        current_theme = pygame.transform.smoothscale(current_theme, (screen_width, screen_height))
        screen.blit(current_theme, (0, 0))

        render_centered_text('Choose Theme', font_large, white, screen_width // 2, screen_height // 2 - 250)

        next_button = pygame.Rect(screen_width // 2 + 100, screen_height // 2, 100, 50)
        prev_button = pygame.Rect(screen_width // 2 - 200, screen_height // 2, 130, 50)
        select_button = pygame.Rect(screen_width // 2-100, screen_height // 2 + 100, 200, 50)

        draw_button(next_button, 'Next')
        draw_button(prev_button, 'Previous')
        draw_button(select_button, 'Select')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if next_button.collidepoint(mouse_pos):
                    theme_index = (theme_index + 1) % len(themes)
                elif prev_button.collidepoint(mouse_pos):
                    theme_index = (theme_index - 1) % len(themes)
                elif select_button.collidepoint(mouse_pos):
                    background_path = themes[theme_index]
                    if os.path.exists(background_path):
                        background = pygame.image.load(background_path)
                        background = pygame.transform.smoothscale(background, (screen_width, screen_height))
                    choosing_theme = False

        pygame.display.flip()

def settings_wd():
    global background_path, background, dark_mode, difficulty
    settings_open = True
    difficulty_message_time = 0
    show_difficulty_message = False

    while settings_open:
        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        render_centered_text('Settings', font_large, white, screen_width // 2, screen_height // 2 - 250)

        volume_options = [
            {"button": pygame.Rect(screen_width // 2 + 50 + 25, screen_height // 2 - 200 + 25, 50, 50), "text": "Background Music"},
            {"button": pygame.Rect(screen_width // 2 + 50 + 25, screen_height // 2 - 125 + 25, 50, 50), "text": "Correct Sound"},
            {"button": pygame.Rect(screen_width // 2 + 50 + 25, screen_height // 2 - 50 + 25, 50, 50), "text": "Wrong Sound"},
            {"button": pygame.Rect(screen_width // 2 + 50 + 25, screen_height // 2 + 25 + 25, 50, 50), "text": "Win Sound"}
        ]
        volume_down_buttons = [
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 200 + 25, 50, 50),
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 125 + 25, 50, 50),
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50 + 25, 50, 50),
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 25 + 25, 50, 50)
        ]

        def get_rounded_volume(volume):
            return round(volume * 10) * 10

        for i, option in enumerate(volume_options):
            draw_button(option["button"], '+')
            render_centered_text(option["text"], font_small, white, option["button"].centerx - 375, option["button"].centery)
            if i == 0:
                volume = get_rounded_volume(background_volume)
            elif i == 1:
                volume = get_rounded_volume(correct_volume)
            elif i == 2:
                volume = get_rounded_volume(wrong_volume)
            elif i == 3:
                volume = get_rounded_volume(win_volume)
            render_centered_text(f'{volume}%', font_small, white, option["button"].centerx - 80, option["button"].centery)

        for button in volume_down_buttons:
            draw_button(button, '-')

        options = [
            {"button": pygame.Rect(screen_width // 2 - 350 - 10, screen_height - 130, 100, 50), "text": "Back"},
            {"button": pygame.Rect(screen_width // 2 - 225 - 10, screen_height - 130, 225, 50), "text": f'Difficulty: {difficulty}'},
            {"button": pygame.Rect(screen_width // 2 + 25 - 10, screen_height - 130, 200, 50), "text": 'Change Theme'},
            {"button": pygame.Rect(screen_width // 2 + 250 - 10, screen_height - 130, 175, 50), "text": 'Toggle Mode'}
        ]

        for option in options:
            draw_button(option["button"], option["text"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, option in enumerate(volume_options):
                    if option["button"].collidepoint(mouse_pos):
                        increase_volume(i)
                for i, button in enumerate(volume_down_buttons):
                    if button.collidepoint(mouse_pos):
                        decrease_volume(i)
                if options[0]["button"].collidepoint(mouse_pos):
                    settings_open = False
                elif options[1]["button"].collidepoint(mouse_pos):
                    show_difficulty_message = True
                    difficulty_message_time = time.time()
                elif options[2]["button"].collidepoint(mouse_pos):
                    change_theme()
                elif options[3]["button"].collidepoint(mouse_pos):
                    dark_mode = not dark_mode

        if show_difficulty_message and time.time() - difficulty_message_time <= 3:
            render_text('Difficulty cannot be changed', screen_width // 2 - 225 , screen_height - 80, font_ss, white)
            render_text(' in between a level', screen_width // 2 - 200, screen_height -50, font_ss, white)
        elif show_difficulty_message:
            show_difficulty_message = False

        pygame.display.flip()
#different setting
def settings():
    global background_path, background, dark_mode, difficulty
    settings_open = True

    while settings_open:
        screen.fill(black if dark_mode else white)
        screen.blit(background, (0, 0))

        render_centered_text('Settings', font_large, white, screen_width // 2, screen_height // 2 - 250)

        volume_options = [
            {"button": pygame.Rect(screen_width // 2 + 50+25, screen_height // 2 - 200+25, 50, 50), "text": "Background Music"},
            {"button": pygame.Rect(screen_width // 2 + 50+25, screen_height // 2 - 125+25, 50, 50), "text": "Correct Sound"},
            {"button": pygame.Rect(screen_width // 2 + 50+25, screen_height // 2 - 50+25, 50, 50), "text": "Wrong Sound"},
            {"button": pygame.Rect(screen_width // 2 + 50+25, screen_height // 2 + 25+25, 50, 50), "text": "Win Sound"}
        ]
        volume_down_buttons = [
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 200+25, 50, 50),
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 125+25, 50, 50),
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50+25, 50, 50),
            pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 25+25, 50, 50)
        ]

        def get_rounded_volume(volume):
            return round(volume * 10) * 10

        for i, option in enumerate(volume_options):
            draw_button(option["button"], '+')
            render_centered_text(option["text"], font_small, white, option["button"].centerx - 375, option["button"].centery)
            if i == 0:
                volume = get_rounded_volume(background_volume)
            elif i == 1:
                volume = get_rounded_volume(correct_volume)
            elif i == 2:
                volume = get_rounded_volume(wrong_volume)
            elif i == 3:
                volume = get_rounded_volume(win_volume)
            render_centered_text(f'{volume}%', font_small, white, option["button"].centerx -80, option["button"].centery)

        for button in volume_down_buttons:
            draw_button(button, '-')

        options = [
            {"button": pygame.Rect(screen_width // 2 - 350 - 10, screen_height - 130, 100, 50), "text": "Back"},
            {"button": pygame.Rect(screen_width // 2 - 225 - 10, screen_height - 130, 225, 50), "text": f'Difficulty: {difficulty}'},
            {"button": pygame.Rect(screen_width // 2 + 25 - 10, screen_height - 130, 200, 50), "text": 'Change Theme'},
            {"button": pygame.Rect(screen_width // 2 + 250 - 10, screen_height - 130, 175, 50), "text": 'Toggle Mode'}
        ]

        for option in options:
            draw_button(option["button"], option["text"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, option in enumerate(volume_options):
                    if option["button"].collidepoint(mouse_pos):
                        increase_volume(i)
                for i, button in enumerate(volume_down_buttons):
                    if button.collidepoint(mouse_pos):
                        decrease_volume(i)
                if options[0]["button"].collidepoint(mouse_pos):
                    settings_open = False
                elif options[1]["button"].collidepoint(mouse_pos):
                    difficulty = 'Easy' if difficulty == 'Hard' else 'Medium' if difficulty == 'Easy' else 'Hard'
                elif options[2]["button"].collidepoint(mouse_pos):
                    change_theme()
                elif options[3]["button"].collidepoint(mouse_pos):
                    dark_mode = not dark_mode

        pygame.display.flip()
        
def increase_volume(index):
    global background_volume, correct_volume, wrong_volume, win_volume
    if index == 0:
        background_volume = min(1.0, background_volume + 0.1)
        pygame.mixer.music.set_volume(background_volume)
    elif index == 1:
        correct_volume = min(1.0, correct_volume + 0.1)
        correct_sound.set_volume(correct_volume)
    elif index == 2:
        wrong_volume = min(1.0, wrong_volume + 0.1)
        wrong_sound.set_volume(wrong_volume)
    elif index == 3:
        win_volume = min(1.0, win_volume + 0.1)
        win_sound.set_volume(win_volume)
    print_volume_status()

def decrease_volume(index):
    global background_volume, correct_volume, wrong_volume, win_volume
    if index == 0:
        background_volume = max(0.0, background_volume - 0.1)
        pygame.mixer.music.set_volume(background_volume)
    elif index == 1:
        correct_volume = max(0.0, correct_volume - 0.1)
        correct_sound.set_volume(correct_volume)
    elif index == 2:
        wrong_volume = max(0.0, wrong_volume - 0.1)
        wrong_sound.set_volume(wrong_volume)
    elif index == 3:
        win_volume = max(0.0, win_volume - 0.1)
        win_sound.set_volume(win_volume)
    print_volume_status()

def print_volume_status():
    print(f"Background Music Volume: {background_volume * 100}%")
    print(f"Correct Sound Volume: {correct_volume * 100}%")
    print(f"Wrong Sound Volume: {wrong_volume * 100}%")
    print(f"Win Sound Volume: {win_volume * 100}%")    
if __name__ == "__main__":
    start()
    


