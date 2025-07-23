import pygame as p
import tohka_admin
WIDTH, HEIGHT = 560, 560
DIMENSION = 8
SQ_SIZE = HEIGHT/DIMENSION
MAX_FPS = 15
IMAGES = {}

pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]


# Load images
def load_images():
    for piece in pieces:
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
def draw_game(surface, gs):
    draw_board(surface)
    draw_piece(surface, gs.board)

# "Actually" display board
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    load_images()
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
                if selected_coor == (r_coor, f_coor):
                    selected_coor = ()
                    player_clicks = []
                else:
                    selected_coor = (r_coor, f_coor)
                    player_clicks.append(selected_coor)

                if len(player_clicks) == 2:
                    move = tohka_admin.Move(start_sq=player_clicks[0], end_sq=player_clicks[1],
                                            game_board=game_state.board)
                    if move in valid_moves:
                        game_state.make_move(move)
                        moved = True
                        selected_coor = ()
                        player_clicks = []
                    else:
                        player_clicks = [selected_coor]

            elif event.type == p.KEYDOWN:
                if event.key == p.K_z 
                    game_state.undo_move()
                    moved = True

        if moved:
            valid_moves = game_state.get_valid_moves()
            moved = False

        screen.fill("white")
        draw_game(screen, game_state)
        p.display.flip()
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
