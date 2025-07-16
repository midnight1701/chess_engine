import pygame as p
import tohka_admin
WIDTH, HEIGHT = 640, 640
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION
MAX_FPS = 15
IMAGES = {}

white_piece = ["wp", "wR", "wN", "wB", "wQ", "wK"]
black_piece = ["bp", "bR", "bN", "bB", "bQ", "bK"]

# Load images
def load_images():
    for piece in white_piece:
        IMAGES[piece] = p.transform.scale(p.image.load("tohka_piece/" + piece + ".png"),
                                          (SQ_SIZE, SQ_SIZE))

    for piece in black_piece:
        IMAGES[piece] = p.transform.scale(p.image.load("tohka_piece/" + piece + ".png"),
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

# "Actually" display board
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    running = True

    game_state = tohka_admin.GameState()
    valid_moves = game_state.get_valid_moves()
    moved = False

    selected_coor = ()
    player_clicks = []

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                r_coor = int(mouse_pos[1] // SQ_SIZE)
                f_coor = int(mouse_pos[0] // SQ_SIZE)
                if (r_coor, f_coor) != selected_coor:
                    selected_coor = (r_coor, f_coor)
                    player_clicks.append(selected_coor)
                else:
                    selected_coor = ()
                    player_clicks = []

                if len(player_clicks) == 2:
                    move = tohka_admin.Move(click_lst=player_clicks, game_board=game_state.board)
                    if move in valid_moves:
                        game_state.make_move(move)
                        moved = True
                        selected_coor = ()
                        player_clicks = []
                    else:
                        player_clicks.pop()

            elif event.type == p.KEYDOWN:
                if event.key == p.K_z and p.key.get_mods() & p.KMOD_CTRL:
                    game_state.undo_move()
                    moved = True

        if moved:
            valid_moves = game_state.get_valid_moves()
            moved = False

        screen.fill("white")
        draw_game(screen, game_state.board)
        p.display.flip()
        clock.tick(MAX_FPS)
    p.quit()


if __name__ == "__main__":
    main()
