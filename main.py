import pygame
import sys
import game_functions as gf  # Import game logic
from ai_player import AIPlayer  # Import AI logic
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Constants
INFO_BAR_HEIGHT = 50  # Height for the info bar at the top
BOTTOM_BAR_HEIGHT = 40  # Height for the bottom bar

SQUARE_WINDOW_GRID = 600
WIDTH, HEIGHT = SQUARE_WINDOW_GRID, SQUARE_WINDOW_GRID + INFO_BAR_HEIGHT + BOTTOM_BAR_HEIGHT
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
SMALL_GRID_SIZE = 3
LINE_WIDTH = 2
WIN_LINE_WIDTH = 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 99, 71)
BLUE = (65, 105, 225)
INFO_BAR_COLOR = (200, 54, 255)
BG_COLOR = (240, 240, 240)
HIGHLIGHT_COLOR = (173, 216, 230)
WIN_COLOR = (50, 205, 50)
DRAW_COLOR = (128, 128, 128)
ACTIVE_GRID_COLOR = (194, 255, 125)

X_WIN_COLOR = (255, 159, 159)
O_WIN_COLOR = (159, 159, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Tic-Tac-Toe")

# Fonts
font_large = pygame.font.Font(None, 90)
font_info = pygame.font.Font(None, 36)
font_button = pygame.font.Font(None, 30)

# Buttons for game over and menu
button_width = 200
button_height = 50
button_spacing = 20

restart_button_rect = pygame.Rect(WIDTH // 2 - button_width - button_spacing // 2, HEIGHT // 2 + 50, button_width,
                                  button_height)
quit_button_rect = pygame.Rect(WIDTH // 2 + button_spacing // 2, HEIGHT // 2 + 50, button_width, button_height)

# Menu buttons
human_vs_human_rect = pygame.Rect(WIDTH // 2 - button_width - button_spacing // 2, HEIGHT // 2 - button_height // 2,
                                  button_width, button_height)
human_vs_ai_rect = pygame.Rect(WIDTH // 2 + button_spacing // 2, HEIGHT // 2 - button_height // 2, button_width,
                               button_height)
toggle_sound_rect = pygame.Rect(WIDTH - 150, HEIGHT - BOTTOM_BAR_HEIGHT + 5, 140, 30)

# Sound settings
sound_on = True
sounds = {}
sounds_dir = os.path.join(os.path.dirname(__file__), 'sounds')
sounds['move_x'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'move_x.mp3'))
sounds['move_o'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'move_o.mp3'))
sounds['win'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'win.mp3'))
sounds['draw'] = pygame.mixer.Sound(os.path.join(sounds_dir, 'draw.mp3'))
pygame.mixer.music.load(os.path.join(sounds_dir, 'background_music.mp3'))
pygame.mixer.music.play(-1)  # Play background music in a loop


# Main Game Function
def main():
    global player1_name, player2_name, ai_player, sound_on

    # Display main menu
    game_mode = display_main_menu()

    # Get player names
    if game_mode == 'human_vs_human':
        player1_name = get_player_name("Enter Player 1 Name: ")
        player2_name = get_player_name("Enter Player 2 Name: ")
        ai_player = None
    elif game_mode == 'human_vs_ai':
        player1_name = get_player_name("Enter Your Name: ")
        player2_name = "AI Player"
        difficulty = select_difficulty()
        ai_player = AIPlayer('O', difficulty=difficulty)  # AI plays as 'O'

    # Initialize game state
    game_state = gf.initialize_game_state()
    board = game_state['board']
    small_boards = game_state['small_boards']
    next_grid = game_state['next_grid']
    winner = game_state['winner']
    game_over = game_state['game_over']
    current_player = game_state['current_player']

    # Introduce a new variable to handle AI thinking state
    ai_thinking = False
    ai_think_start_time = 0

    running = True
    while running:
        screen.fill(BG_COLOR)

        if not game_over:
            # Highlight the active grid
            highlight_active_grid(next_grid)

            # Draw the grid and game info
            draw_grid(small_boards)
            display_game_info(current_player, player1_name,
                              player2_name, next_grid)
            display_bottom_info(ai_thinking)  # Show AI thinking on bottom bar

            # Draw moves on the grid
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if board[row][col] is not None:
                        draw_move(row, col, board)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if toggle_sound_rect.collidepoint(x, y):
                        sound_on = not sound_on
                        if sound_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    elif (current_player == 'X' or
                          (current_player == 'O' and ai_player is None)):
                        # Human player's turn
                        row = (y - INFO_BAR_HEIGHT) // CELL_SIZE
                        col = x // CELL_SIZE
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            small_grid_row = row // SMALL_GRID_SIZE
                            small_grid_col = col // SMALL_GRID_SIZE
                            if (next_grid is None or
                                next_grid == (small_grid_row, small_grid_col)):
                                if board[row][col] is None:
                                    # Make the move
                                    next_grid = gf.make_move(
                                        board, small_boards, row, col,
                                        current_player)
                                    if sound_on:
                                        sounds['move_x' if current_player == 'X'
                                               else 'move_o'].play()
                                    # Check for win/draw
                                    if gf.check_super_grid_win(
                                            small_boards, current_player):
                                        winner = current_player
                                        game_over = True
                                        if sound_on:
                                            sounds['win'].play()
                                    elif gf.check_draw(small_boards):
                                        winner = 'Draw'
                                        game_over = True
                                        if sound_on:
                                            sounds['draw'].play()
                                    else:
                                        # Switch player
                                        current_player = ('O' if
                                                          current_player == 'X'
                                                          else 'X')
                                        if (current_player == 'O' and
                                            ai_player is not None):
                                            ai_thinking = True
                                            ai_think_start_time = pygame.time.get_ticks()

            # Handle AI thinking and move
            if ai_thinking and (pygame.time.get_ticks() - ai_think_start_time > 500):
                # AI's turn
                move = ai_player.make_move(board, small_boards, next_grid)
                if move is not None:
                    row, col = move
                    next_grid = gf.make_move(board, small_boards, row, col,
                                             current_player)
                    if sound_on:
                        sounds['move_o'].play()
                    # Check for win/draw
                    if gf.check_super_grid_win(small_boards, current_player):
                        winner = current_player
                        game_over = True
                        if sound_on:
                            sounds['win'].play()
                    elif gf.check_draw(small_boards):
                        winner = 'Draw'
                        game_over = True
                        if sound_on:
                            sounds['draw'].play()
                    else:
                        # Switch player
                        current_player = 'X'
                ai_thinking = False

        else:
            # Game over screen
            display_game_over(winner, player1_name, player2_name)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Check if buttons are clicked
                    if restart_button_rect.collidepoint(x, y):
                        # Restart the game
                        game_state = gf.initialize_game_state()
                        board = game_state['board']
                        small_boards = game_state['small_boards']
                        next_grid = game_state['next_grid']
                        winner = game_state['winner']
                        game_over = game_state['game_over']
                        current_player = game_state['current_player']
                        ai_thinking = False
                    elif quit_button_rect.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()


# Function to display the main menu and return game mode
def display_main_menu():
    while True:
        screen.fill(BG_COLOR)

        # Draw buttons
        pygame.draw.rect(screen, BLUE, human_vs_human_rect)
        pygame.draw.rect(screen, RED, human_vs_ai_rect)

        # Draw button text
        hvh_text = font_button.render("Human vs Human", True, WHITE)
        hvh_rect = hvh_text.get_rect(center=human_vs_human_rect.center)
        screen.blit(hvh_text, hvh_rect)

        hvsai_text = font_button.render("Human vs AI", True, WHITE)
        hvsai_rect = hvsai_text.get_rect(center=human_vs_ai_rect.center)
        screen.blit(hvsai_text, hvsai_rect)

        # Sound toggle button
        draw_sound_toggle_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if toggle_sound_rect.collidepoint(x, y):
                    global sound_on
                    sound_on = not sound_on
                    if sound_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif human_vs_human_rect.collidepoint(x, y):
                    return 'human_vs_human'
                elif human_vs_ai_rect.collidepoint(x, y):
                    return 'human_vs_ai'


# Function to get player name input
def get_player_name(prompt):
    name = ""
    entering_name = True
    while entering_name:
        screen.fill(BG_COLOR)

        # Render the prompt
        prompt_surface = font_info.render(prompt + name, True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(prompt_surface, prompt_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name or "Player"


# Function to select AI difficulty
def select_difficulty():
    difficulties = ['Easy', 'Medium', 'Hard']
    selected = 1  # Default to Medium
    selecting = True
    while selecting:
        screen.fill(BG_COLOR)

        # Render the prompt
        prompt_surface = font_info.render("Select AI Difficulty:", True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(prompt_surface, prompt_rect)

        # Render difficulty options
        for i, diff in enumerate(difficulties):
            color = BLUE if i == selected else BLACK
            diff_surface = font_button.render(diff, True, color)
            diff_rect = diff_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40))
            screen.blit(diff_surface, diff_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    selecting = False
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
    return difficulties[selected].lower()


# Modify display_game_info function to show usual info on top
def display_game_info(current_player, player_one_name, player_two_name, next_grid):
    pygame.draw.rect(screen, INFO_BAR_COLOR,
                     pygame.Rect(0, 0, WIDTH, INFO_BAR_HEIGHT))
    current_player_name = (player_one_name if current_player == 'X'
                           else player_two_name)
    info_text = f"Current Player: {current_player_name} ({current_player})"
    if next_grid is not None:
        info_text += (f" | Play in Grid ({next_grid[0] + 1}, "
                      f"{next_grid[1] + 1})")
    else:
        info_text += " | Play in Any Grid"
    text_surface = font_info.render(info_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, INFO_BAR_HEIGHT // 2))
    screen.blit(text_surface, text_rect)


# Add new function to display AI thinking on bottom bar
def display_bottom_info(ai_thinking=False):
    pygame.draw.rect(screen, INFO_BAR_COLOR,
                     pygame.Rect(0, HEIGHT - BOTTOM_BAR_HEIGHT, WIDTH, BOTTOM_BAR_HEIGHT))

    if ai_thinking:
        ai_text = "AI Player is thinking..."
        ai_text_surface = font_button.render(ai_text, True, BLACK)
        ai_text_rect = ai_text_surface.get_rect(midleft=(10, HEIGHT - BOTTOM_BAR_HEIGHT // 2))
        screen.blit(ai_text_surface, ai_text_rect)

    # Draw sound toggle button on bottom bar
    draw_sound_toggle_button()


# Function to draw the game grid and small board highlights
def draw_grid(small_boards):
    # Loop through each small 3x3 grid and check for wins
    for grid_row in range(SMALL_GRID_SIZE):
        for grid_col in range(SMALL_GRID_SIZE):
            if small_boards[grid_row][grid_col] == 'X':
                # X won this small board
                top_left_x = grid_col * CELL_SIZE * SMALL_GRID_SIZE
                top_left_y = grid_row * CELL_SIZE * SMALL_GRID_SIZE + INFO_BAR_HEIGHT
                pygame.draw.rect(screen, X_WIN_COLOR,
                                 (top_left_x, top_left_y, SMALL_GRID_SIZE * CELL_SIZE, SMALL_GRID_SIZE * CELL_SIZE))
            elif small_boards[grid_row][grid_col] == 'O':
                # O won this small board
                top_left_x = grid_col * CELL_SIZE * SMALL_GRID_SIZE
                top_left_y = grid_row * CELL_SIZE * SMALL_GRID_SIZE + INFO_BAR_HEIGHT
                pygame.draw.rect(screen, O_WIN_COLOR,
                                 (top_left_x, top_left_y, SMALL_GRID_SIZE * CELL_SIZE, SMALL_GRID_SIZE * CELL_SIZE))

    # Draw lines for the main grid
    for x in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, INFO_BAR_HEIGHT), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE + INFO_BAR_HEIGHT), (WIDTH, x * CELL_SIZE + INFO_BAR_HEIGHT),
                         LINE_WIDTH)

    # Draw thick lines for the super grid
    for i in range(1, SMALL_GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * WIDTH // SMALL_GRID_SIZE, INFO_BAR_HEIGHT),
                         (i * WIDTH // SMALL_GRID_SIZE, HEIGHT), WIN_LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, i * WIDTH // SMALL_GRID_SIZE + INFO_BAR_HEIGHT),
                         (WIDTH, i * WIDTH // SMALL_GRID_SIZE + INFO_BAR_HEIGHT), WIN_LINE_WIDTH)


# Function to draw X or O moves
def draw_move(row, col, board):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2 + INFO_BAR_HEIGHT
    if board[row][col] == 'X':
        pygame.draw.line(screen, RED, (center_x - CELL_SIZE // 3, center_y - CELL_SIZE // 3),
                         (center_x + CELL_SIZE // 3, center_y + CELL_SIZE // 3), LINE_WIDTH)
        pygame.draw.line(screen, RED, (center_x + CELL_SIZE // 3, center_y - CELL_SIZE // 3),
                         (center_x - CELL_SIZE // 3, center_y + CELL_SIZE // 3), LINE_WIDTH)
    elif board[row][col] == 'O':
        pygame.draw.circle(screen, BLUE, (center_x, center_y), CELL_SIZE // 3, LINE_WIDTH)


# Highlight the active grid for the next move
def highlight_active_grid(next_grid):
    if next_grid is not None:
        grid_row, grid_col = next_grid
        top_left_x = grid_col * CELL_SIZE * SMALL_GRID_SIZE
        top_left_y = grid_row * CELL_SIZE * SMALL_GRID_SIZE + INFO_BAR_HEIGHT
        pygame.draw.rect(screen, ACTIVE_GRID_COLOR,
                         (top_left_x, top_left_y, SMALL_GRID_SIZE * CELL_SIZE, SMALL_GRID_SIZE * CELL_SIZE))


# Display the game over screen
def display_game_over(winner, player_one_name, player_two_name):
    screen.fill(BG_COLOR)
    if winner == 'Draw':
        message = "Game is a Draw!"
        color = DRAW_COLOR
    else:
        winner_name = player_one_name if winner == 'X' else player_two_name
        message = f"{winner_name} Wins!"
        color = WIN_COLOR

    text_surface = font_large.render(message, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    # Draw buttons
    pygame.draw.rect(screen, BLUE, restart_button_rect)
    pygame.draw.rect(screen, RED, quit_button_rect)

    # Draw button text
    restart_text = font_button.render("Restart Game", True, WHITE)
    restart_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_rect)

    quit_text = font_button.render("Quit Game", True, WHITE)
    quit_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()


# Draw sound toggle button
def draw_sound_toggle_button():
    pygame.draw.rect(screen, INFO_BAR_COLOR, toggle_sound_rect)
    sound_text = "Sound: On" if sound_on else "Sound: Off"
    sound_surface = font_button.render(sound_text, True, BLACK)
    sound_rect = sound_surface.get_rect(center=toggle_sound_rect.center)
    screen.blit(sound_surface, sound_rect)


# Run the main game loop
if __name__ == "__main__":
    main()



