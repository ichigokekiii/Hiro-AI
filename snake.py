#!/usr/bin/env python3
"""Simple Snake desktop game built with pygame."""

import random
import sys

import pygame

CELL_SIZE = 24
GRID_WIDTH = 24
GRID_HEIGHT = 18
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 40

BG_COLOR = (18, 18, 24)
SNAKE_COLOR = (76, 217, 100)
SNAKE_HEAD_COLOR = (52, 199, 89)
FOOD_COLOR = (255, 95, 86)
TEXT_COLOR = (240, 240, 245)
GRID_COLOR = (30, 30, 38)

FPS = 10


def random_food(snake):
    while True:
        pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if pos not in snake:
            return pos


def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, GRID_HEIGHT * CELL_SIZE))
    for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))


def draw_cell(surface, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=4)


def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("dejavusans", 22)
    big_font = pygame.font.SysFont("dejavusans", 36, bold=True)

    direction = (1, 0)
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    food = random_food(snake)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

                if game_over and event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                    direction = (1, 0)
                    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                    food = random_food(snake)
                    score = 0
                    game_over = False
                    continue

                if not game_over:
                    if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                        direction = (1, 0)

        if not game_over:
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            if (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
                or new_head in snake
            ):
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        screen.fill(BG_COLOR)
        draw_grid(screen)

        for index, segment in enumerate(snake):
            color = SNAKE_HEAD_COLOR if index == 0 else SNAKE_COLOR
            draw_cell(screen, segment, color)

        draw_cell(screen, food, FOOD_COLOR)

        score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_surface, (12, GRID_HEIGHT * CELL_SIZE + 8))

        help_surface = font.render("Arrows/WASD • R to restart • Esc to quit", True, TEXT_COLOR)
        help_rect = help_surface.get_rect(right=SCREEN_WIDTH - 12, top=GRID_HEIGHT * CELL_SIZE + 8)
        screen.blit(help_surface, help_rect)

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, GRID_HEIGHT * CELL_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title = big_font.render("Game Over", True, TEXT_COLOR)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, GRID_HEIGHT * CELL_SIZE // 2 - 20))
            screen.blit(title, title_rect)

            subtitle = font.render("Press R or Space to play again", True, TEXT_COLOR)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, GRID_HEIGHT * CELL_SIZE // 2 + 20))
            screen.blit(subtitle, subtitle_rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
