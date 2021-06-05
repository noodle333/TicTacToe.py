import pygame
import sys
import numpy as np

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 8
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

BG_COLOR = (165, 232, 158)
LINE_COLOR = (123, 173, 118)
WHITE = (255, 255, 255)

surface = pygame.display.set_mode((200, 200))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)

# init board
board = np.zeros((BOARD_ROWS, BOARD_COLS))


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, LINE_COLOR, (int(
                    col*200 + 200 / 2), int(row*200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, WHITE, (col*200 + SPACE, row*200 + 200 - SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)


def draw_board():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)


def mark_square(row, col, player):
    board[row][col] = player


def empty_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def check_win(player):
    # vertical
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_win(col, player)
            return True
    # horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_win(row, player)
            return True

    # diagonal A
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_diagonal_win_A(player)
        return True

    # diagonal B
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_diagonal_win_B(player)
        return True

    return False

def check_draw():
    if is_board_full() and not check_win(1) and not check_win(2):
        return True

def draw_vertical_win(col, player):
    posX = col * 200 + 100

    if player == 1:
        color = LINE_COLOR
    elif player == 2:
        color = WHITE

    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)


def draw_horizontal_win(row, player):
    posY = row * 200 + 100

    if player == 1:
        color = LINE_COLOR
    elif player == 2:
        color = WHITE

    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)


def draw_diagonal_win_A(player):
    if player == 1:
        color = LINE_COLOR
    elif player == 2:
        color = WHITE

    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)


def draw_diagonal_win_B(player):
    if player == 1:
        color = LINE_COLOR
    elif player == 2:
        color = WHITE

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)


def restart():
    screen.fill(BG_COLOR)
    draw_board()
    player = 1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


draw_board()
player = 1

game_over = False

# main game loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = e.pos[0]
            mouseY = e.pos[1]

            clicked_row = int(mouseY // 200)
            clicked_col = int(mouseX // 200)

            if empty_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    if check_win(player):
                        game_over = True
                    if check_draw():
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    if check_win(player):
                        game_over = True
                    if check_draw():
                        game_over = True
                    player = 1

                draw_figures()
            print(board)

        if e.type == pygame.KEYDOWN and game_over:
            restart()
            game_over = False

    # updates the screen
    pygame.display.update()
