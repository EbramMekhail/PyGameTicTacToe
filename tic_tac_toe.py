import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH = 600
HEIGHT = 600
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set font
FONT = pygame.font.SysFont(None, 40)

# Create game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Initialize game variables
player_turn = None
game_over = False
winner = None
board = [[None, None, None],
         [None, None, None],
         [None, None, None]]


def draw_board():
    window.fill(WHITE)
    pygame.draw.line(window, BLACK, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(window, BLACK, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), 5)
    pygame.draw.line(window, BLACK, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), 5)
    pygame.draw.line(window, BLACK, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), 5)

    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                x1 = col * WIDTH // 3 + WIDTH // 6 - 40
                y1 = row * HEIGHT // 3 + HEIGHT // 6 - 40
                x2 = col * WIDTH // 3 + WIDTH // 6 + 40
                y2 = row * HEIGHT // 3 + HEIGHT // 6 + 40
                pygame.draw.line(window, RED, (x1, y1), (x2, y2), 5)
                pygame.draw.line(window, RED, (x1, y2), (x2, y1), 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(window, GREEN, (col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6),
                                   min(WIDTH, HEIGHT) // 12, 5)


def check_winner():
    global game_over
    global winner

    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            game_over = True
            winner = board[row][0]
            return

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            game_over = True
            winner = board[0][col]
            return

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        winner = board[0][0]
        return

    if board[2][0] == board[1][1] == board[0][2] and board[2][0] is not None:
        game_over = True
        winner = board[2][0]
        return

    # Check for tie
    if all(board[row][col] is not None for row in range(3) for col in range(3)):
        game_over = True
        winner = None


def reset_game():
    global player_turn
    global game_over
    global winner
    global board

    player_turn = random.choice(['X', 'O'])
    game_over = False
    winner = None
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]


def draw_start_menu():
    window.fill(WHITE)
    text = FONT.render("Tic Tac Toe", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    window.blit(text, text_rect)

    play_human_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
    play_bot_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
                                  BUTTON_WIDTH, BUTTON_HEIGHT)

    pygame.draw.rect(window, BLACK, play_human_button)
    pygame.draw.rect(window, BLACK, play_bot_button)

    text = FONT.render("Play Against a Human", True, WHITE)
    text_rect = text.get_rect(center=play_human_button.center)
    window.blit(text, text_rect)

    text = FONT.render("Play Against Bot", True, WHITE)
    text_rect = text.get_rect(center=play_bot_button.center)
    window.blit(text, text_rect)

    return play_human_button, play_bot_button


def draw_game_over_screen():
    window.fill(WHITE)
    if winner:
        text = FONT.render(f"{winner} Wins!", True, BLACK)
    else:
        text = FONT.render("It's a Tie!", True, BLACK)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(text, text_rect)

    rematch_button = pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN,
                                 BUTTON_WIDTH, BUTTON_HEIGHT)

    pygame.draw.rect(window, BLACK, rematch_button)

    text = FONT.render("Rematch", True, WHITE)
    text_rect = text.get_rect(center=rematch_button.center)
    window.blit(text, text_rect)

    return rematch_button


def play_vs_human():
    global player_turn

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = x // (WIDTH // 3)
                row = y // (HEIGHT // 3)

                if board[row][col] is None:
                    board[row][col] = player_turn
                    check_winner()
                    if not game_over:
                        player_turn = 'O' if player_turn == 'X' else 'X'

        draw_board()
        pygame.display.flip()

    rematch_button = draw_game_over_screen()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if rematch_button.collidepoint(x, y):
                    reset_game()
                    draw_board()
                    pygame.display.flip()
                    return

        pygame.display.flip()


def play_vs_bot():
    global player_turn

    bot_turn = random.choice(['X', 'O'])
    while not game_over:
        if player_turn == bot_turn:
            # Bot's turn
            available_moves = [(row, col) for row in range(3) for col in range(3) if board[row][col] is None]
            if available_moves:
                row, col = random.choice(available_moves)
                board[row][col] = player_turn
                check_winner()
                player_turn = 'X' if player_turn == 'O' else 'O'
        else:
            # Player's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    col = x // (WIDTH // 3)
                    row = y // (HEIGHT // 3)

                    if board[row][col] is None:
                        board[row][col] = player_turn
                        check_winner()
                        player_turn = 'X' if player_turn == 'O' else 'O'

        draw_board()
        pygame.display.flip()

    rematch_button = draw_game_over_screen()

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if rematch_button.collidepoint(x, y):
                    reset_game()
                    draw_board()
                    pygame.display.flip()
                    return

        pygame.display.flip()


def main():
    play_human_button, play_bot_button = draw_start_menu()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if play_human_button.collidepoint(x, y):
                    reset_game()
                    play_vs_human()
                    play_human_button, play_bot_button = draw_start_menu()
                elif play_bot_button.collidepoint(x, y):
                    reset_game()
                    play_vs_bot()
                    play_human_button, play_bot_button = draw_start_menu()

        pygame.display.flip()


if __name__ == '__main__':
    main()
