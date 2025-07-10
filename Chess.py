import pygame as p
from ChessEngine import GameState

WIDTH, HEIGHT = 640, 640
DIMENSION = 8
SQ_SIZE = HEIGHT/ DIMENSION
MAX_FPS = 15
IMAGES = {}

white_piece = ["wp", "wR", "wN", "wB", "wQ", "wK"]
black_piece = ["bp", "bR", "bN", "bB", "bQ", "bK"]

# Load images
def load_images():
    for piece in white_piece:
        IMAGES[piece] = p.transform.scale(p.image.load("ChessPiece/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))

    for piece in black_piece:
        IMAGES[piece] = p.transform.scale(p.image.load("ChessPiece/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))

# Initialize chess board
def draw_board(surface):
    color = [(255, 255, 255), (128, 128, 128)]
    for r in range(DIMENSION):
        for f in range(DIMENSION):
            c = color[(r + f) % 2]
            p.draw.rect(surface, c, p.Rect(r * SQ_SIZE, f * SQ_SIZE, WIDTH, HEIGHT))

# Set up chess piece in board
def draw_piece(surface, game=None):
    for r in range(DIMENSION):
        for f in range(DIMENSION):
            piece = game[f][r]
            if piece != "--":
                surface.blit(IMAGES[piece], p.Rect(r * SQ_SIZE, f * SQ_SIZE, WIDTH, HEIGHT))

# Display board
def draw_game(surface, game):
    gs = game
    load_images()
    draw_board(surface)
    draw_piece(surface, gs)

# "Actually" display board
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    running = True

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        screen.fill("white")
        game_state = ChessEngine.GameState()
        draw_game(screen, game_state.board)
        p.display.flip()
        clock.tick(MAX_FPS)
    p.quit()


if __name__ == "__main__":
    main()
