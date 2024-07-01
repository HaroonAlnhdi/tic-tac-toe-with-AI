
#Haroon Ali Mohammed 202008391

import os
import pygame
import sys
import time

import TicTacToe as XO

pygame.init()
size = width, height = 700, 500

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (173, 216, 230)
gray = (211, 211, 211)

screen = pygame.display.set_mode(size)

# Paths to fonts
script_dir = os.path.dirname(__file__)
font_path = os.path.join(script_dir, "OpenSans-Regular.ttf")

mediumFont = pygame.font.Font(font_path, 28)
largeFont = pygame.font.Font(font_path, 40)
moveFont = pygame.font.Font(font_path, 60)

user = None
board = XO.initial_state()
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)

    # Let user choose a player.
    if user is None:
        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe (X-O Game)", True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, light_blue, playXButton)
        pygame.draw.rect(screen, blue, playXButton, 3)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, light_blue, playOButton)
        pygame.draw.rect(screen, blue, playOButton, 3)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = XO.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = XO.O

    else:
        # Draw game board
        tile_size = 100
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, black, rect, 3)

                if board[i][j] != XO.EMPTY:
                    move = moveFont.render(board[i][j], True, red if board[i][j] == XO.X else green)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = XO.terminal(board)
        player = XO.player(board)

        # Show title
        if game_over:
            winner = XO.winner(board)
            if winner is None:
                title = "Game Over: Tie."
                title_color = gray
            else:
                title = f"Game Over: {winner} wins."
                title_color = red if winner == XO.X else green
        elif user == player:
            title = f"Play as {user}"
            title_color = black
        else:
            title = "Computer thinking..."
            title_color = white
        title = largeFont.render(title, True, title_color)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = XO.minimax(board)
                board = XO.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if board[i][j] == XO.EMPTY and tiles[i][j].collidepoint(mouse):
                        board = XO.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, light_blue, againButton)
            pygame.draw.rect(screen, blue, againButton, 3)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = XO.initial_state()
                    ai_turn = False

    pygame.display.flip()
