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
    for r in range(DIMENSION - 1, -1, -1):
        for f in range(DIMENSION):
            piece = game[r][f]
            if piece != "--":
                surface.blit(IMAGES[piece], p.Rect(f * SQ_SIZE, r * SQ_SIZE, WIDTH, HEIGHT))

# Display board
def draw_game(surface, game):
    gs = game
    load_images()
    draw_board(surface)
    draw_piece(surface, gs)

# Display coordinates on chess board
def chess_coordinates(ori_rank, ori_file):
    rank = {1: "8", 2: "7", 3: "6", 4: "5", 5: "4", 6: "3", 7: "2", 8: "1"}
    file = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    r = rank[ori_rank]
    f = file[ori_file]
    print(f + r)

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
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                r_coor = int(mouse_pos[1] // SQ_SIZE) + 1
                f_coor = int(mouse_pos[0] // SQ_SIZE) + 1
                chess_coordinates(r_coor, f_coor)

        screen.fill("white")
        game_state = ChessEngine.GameState()
        draw_game(screen, game_state.board)
        p.display.flip()
        clock.tick(MAX_FPS)
    p.quit()


if __name__ == "__main__":
    main()
