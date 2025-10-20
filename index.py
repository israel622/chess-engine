import chess
import chess.engine
import pygame
import pygame.display
import os


pygame.init()


WINDOW_SIZE = 600
BOARD_SIZE = 400
SQUARE_SIZE = BOARD_SIZE // 8


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_SQUARE = (181, 136, 99)
LIGHT_SQUARE = (240, 217, 181)
TEXT_COLOR = (200, 200, 200)


screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Israel's Chess Game")


PIECES = {}
white_piece_chars = 'PRNBQK'
black_piece_chars = 'prnbqk'
for piece in white_piece_chars:
        img_path = os.path.join('white_pieces', f'{piece}.png')
        PIECES[piece] = pygame.image.load(img_path)
        PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))  
        
for piece in black_piece_chars:
        img_path = os.path.join('black_pieces', f'{piece}.png')
        PIECES[piece] = pygame.image.load(img_path)
        PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))
   

board = chess.Board()
game_moves = []
current_turn = "engine"

MARGIN = 30
BOARD_X_OFFSET = (WINDOW_SIZE - BOARD_SIZE) // 2
BOARD_Y_OFFSET = (WINDOW_SIZE - BOARD_SIZE) // 2


pygame.font.init()
font = pygame.font.SysFont('Arial', 18, bold=True)

def handle_user_move():
    user_input = input("Enter your move : ")
    move = chess.Move.from_uci(user_input)
    if move not in board.legal_moves:
        print("enter a valid move")
        return
    board.push(move)
    game_moves.append(user_input)
    global current_turn
    current_turn = "engine"

def handle_engine_move(engine): 
        result = engine.play(board, chess.engine.Limit(time=0.1))
        move = result.move
        board.push(move)
        game_moves.append(move.uci())
        global current_turn
        current_turn = "user"
    
        
def draw_board():
    for row in range(8):
        for col in range(8):
            x = (WINDOW_SIZE - BOARD_SIZE) // 2 + col * SQUARE_SIZE
            y = (WINDOW_SIZE - BOARD_SIZE) // 2 + row * SQUARE_SIZE
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            x = (WINDOW_SIZE - BOARD_SIZE) // 2 + (square % 8) * SQUARE_SIZE
            y = (WINDOW_SIZE - BOARD_SIZE) // 2 + (7 - square // 8) * SQUARE_SIZE
            if piece.symbol() in PIECES:
                screen.blit(PIECES[piece.symbol()], (x, y))

def draw_labels():
    files = 'abcdefgh'
    ranks = '87654321'

    for i in range(8):
        label_text = font.render(files[i], True, TEXT_COLOR)
        label_rect = label_text.get_rect(center=(
            BOARD_X_OFFSET + i * SQUARE_SIZE + SQUARE_SIZE // 2,
            BOARD_Y_OFFSET + BOARD_SIZE + MARGIN // 2
        ))
        screen.blit(label_text, label_rect)
        
    
    for i in range(8):
        label_text = font.render(ranks[i], True, TEXT_COLOR)
        label_rect = label_text.get_rect(center=(
            BOARD_X_OFFSET - MARGIN // 2,
            BOARD_Y_OFFSET + i * SQUARE_SIZE + SQUARE_SIZE // 2
        ))
        screen.blit(label_text, label_rect)


def update_display():
    screen.fill(GRAY)
    draw_board()
    draw_pieces()
    draw_labels()
    pygame.display.flip()

def main():
    engine_path = "C:\\Users\\user\\Documents\\chess-engine\\stockfish\\stockfish-windows-x86-64-avx2.exe"
    
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        running = True
        while running and not board.is_game_over():
            update_display()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            if current_turn == "engine":
                handle_engine_move(engine)
                print("Engine played:")
                print(board)
                update_display()
                pygame.time.wait(500) 
            
            if running and not board.is_game_over():
                handle_user_move()
                print("User played")
                print(board)
                update_display()
                
                if not board.is_game_over():
                    handle_engine_move(engine)
                    print("Engine played")
                    print(board)
                    update_display()
                    pygame.time.wait(500) 
    
    pygame.quit()


if __name__ == "__main__":
    main()

