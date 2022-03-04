"""
CHESS engine by K.Nariman
Starting date: 15/2/2021

Currently working on the Game mechanics, implementing chess rules, movements, enpassant, castling, capture etc.
In privious version i attempted to design the code oly by using the functions but as the code growed i ended up
using too many on the go variables and globals, so i am redesigning the code and incapsulating.

Graphics done by Pygame, simple stuff, no comment neccessary.
"""

from assets import *

#-- Simple sprite class responsible for pieces
class Piece(pygame.sprite.Sprite):
   def __init__(self, x,y, width,height, image):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x,self.y

"""
Engine class responsible for all attributes and methods, including Data board, current board, temp board and game state.
"""
class Engine():
    def __init__(self):
        #-- Position test board
        self.board = [["BR","--","--","BQ","--","--","--","BR"],# 0
                      ["--","--","--","--","--","--","--","--"],# 1
                      ["--","--","--","--","--","--","--","--"],# 2
                      ["--","--","--","--","BP","BK","--","--"],# 3
                      ["--","--","WP","--","--","--","--","--"],# 4
                      ["--","--","--","--","--","--","--","--"],# 5
                      ["--","--","WB","--","--","--","--","--"],# 4
                      ["WR","--","--","WQ","WK","--","--","WR"] # 7
			         #- 0	1	 2	  3	   4    5    6    7
		               ]

        # self.board = [["BR","BN","BB","BQ","BK","BB","BN","BR"],# 0
        #               ["BP","BP","BP","BP","BP","BP","BP","BP"],# 1
        #               ["--","--","--","--","--","--","--","--"],# 2
        #               ["--","--","--","--","--","--","--","--"],# 3
        #               ["--","--","--","--","--","--","--","--"],# 4
        #               ["--","--","--","--","--","--","--","--"],# 5
        #               ["WP","WP","WP","WP","WP","WP","WP","WP"],# 6
        #               ["WR","WN","WB","WQ","WK","WB","WN","WR"] # 7
        #              #- 0	1	 2	  3	   4    5    6    7
        #              ]

        self.databoard = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                          (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
                          (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),
                          (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),
                          (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),
                          (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),
                          (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),
                          (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]

        self.attempt_to_short_castle = False
        self.attempt_to_long_castle = False
        self.WK_short_castle = True
        self.WK_long_castle = True
        self.BK_short_castle = True
        self.BK_long_castle = True
        self.white_castle = True
        self.black_castle = True
        self.freeze_on_checke = False
        self.check_switches = []
        self.check_log = []
        self.game_state = []
        self.temp_board = []
        self.game_log = []
        self.squares_to_check = []
        self.move = []
        self.white_turn = True
        self.start_square = ""
        self.selected_piece = ""
        self.target_square = ""
        self.target_piece = ""
        self.ss_row = 0
        self.ss_col = 0
        self.ts_row = 0
        self.ts_col = 0
        self.squares_to_check = []
        self.wk_pos = (7,4)
        self.bk_pos = (0,4)
        #-- interface related attributes
        self.all_pieces = pygame.sprite.Group()

    """
    Keep a track of Kings and rooks positions
    """
    def game_update(self):
        for row in self.board:
            r = self.board.index(row)
            for col in row:
                c = row.index(col)
                if self.board[r][c] =="WK":
                    self.wk_pos = (r,c)

                if self.board[r][c] == "BK":
                    self.bk_pos = (r,c)
        #-- Original positions of the pieces at the beginning of the game
        if len(self.game_log) >0:
            for move in self.game_log:
                if "WK" in move:
                    self.white_castle = False
                if "BK" in move:
                    self.black_castle = False
                if "WR" in move and board[7][7] != "WR":
                    self.WK_short_castle = False
                if "WR" in move and board[7][0] != "WR":
                    self.WK_long_castle = False
                if "BR" in move and board[0][7] != "BR":
                    self.BK_short_castle = False
                if "BR" in move and board[0][0] != "BR":
                    self.BK_long_castle = False
        else:
            self.white_castle = True
            self.black_castle = True
            self.WK_short_castle = True
            self.WK_long_castle = True
            self.BK_short_castle = True
            self.BK_long_castle = True


    def pawn_rules(self):
        print("In Pawn function")
        print(self.selected_piece)
        if self.selected_piece[0] == "W":
            # Check if requested move is a first 2 square pawn move
            # prevent pawn to move diagonal
            print(self.ss_row, self.ss_col, self.ts_row, self.ts_col)
            if self.ss_row - self.ts_row == 2 and self.ss_col == self.ts_col:
                if self.ss_row == 6:
                    if self.board[self.ss_row-1][self.ss_col] == "--" and self.board[self.ts_row][self.ts_col] == "--":
                        self.make_move()
            elif self.ss_row - self.ts_row == 1 and self.ss_col == self.ts_col:
                if self.board[self.ts_row][self.ts_col] == "--":
                    self.make_move()

            #-- Capturing
            if self.ts_col - 1 == self.ss_col or self.ts_col + 1 == self.ss_col and self.ts_row+1 == self.ss_row:
                if self.board[self.ts_row][self.ts_col] == "--":
                    if self.ss_row == 3:
                        #-- Enpassant algorithmg
                        #-- Step 1
                        last_move = self.game_log[-1]
                        last_ss_row = last_move[0]
                        last_ss_col = last_move[1]
                        last_ts_row = last_move[2]
                        last_ts_col = last_move[3]
                        last_start_piece = board[last_ss_row][last_ss_col]
                        last_target_piece = board[last_ts_row][last_ts_col]

                        if last_target_piece == "BP":
                            #-- Step 2
                            if last_ss_row + 2 == last_ts_row:
                                #-- Step 3
                                if last_ss_col -1 == self.ss_col:
                                    if self.ss_row != self.ts_row:
                                        if self.ts_col -1 == self.ss_col and self.ts_row+1 == self.ss_row:
                                            print("Right side Enpassant")
                                            start_piece = self.board[self.ss_row][self.ss_col]
                                            self.board[self.ss_row][self.ss_col] = "--"
                                            self.board[self.ts_row+1][self.ts_col] = "--"
                                            self.board[self.ts_row][self.ts_col] = self.selected_piece
                                            self.game_log.append((self.ss_row, self.ss_col, self.ts_row, self.ts_col, self.board[self.ss_row][self.ss_col], self.board[self.ts_row][self.ts_col],"enpassant"))
                                            self.print_board()
                                        else:
                                            print("Wrong enpassant")

                                elif last_ss_col + 1 == self.ss_col:
                                    if self.ss_row != self.ts_row:
                                        if self.ts_col +1 == self.ss_col and self.ts_row+1 == self.ss_row:
                                            print("Light side Enpassant")
                                            start_piece = self.board[self.ss_row][self.ss_col]
                                            self.board[self.ss_row][self.ss_col] = "--"
                                            self.board[self.ts_row+1][self.ts_col] = "--"
                                            self.board[self.ts_row][self.ts_col] = self.selected_piece
                                            self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ss_row][self.ss_col], self.board[self.ts_row][self.ts_col],"enpassant"))
                                            self.print_board()

                elif self.board[self.ts_row][self.ts_col] != "--" and self.ss_row != self.ts_row:
                    self.make_move()

        #-- Black
        elif self.selected_piece[0] == "B":
            # Check if requested move is a first 2 square pawn move
            # prevent pawn to move diagonal
            if self.ts_row - self.ss_row == 2 and self.ss_col == self.ts_col:
                if self.ss_row == 1:
                    if self.board[self.ss_row+1][self.ss_col] == "--" and self.board[self.ts_row][self.ts_col] == "--":
                        self.make_move()
            elif self.ts_row - self.ss_row == 1 and self.ss_col == self.ts_col:
                if self.board[self.ts_row][self.ts_col] == "--":
                    self.make_move()
            #-- Capturing
            if self.ts_col - 1 == self.ss_col or self.ts_col + 1 == self.ss_col and self.ts_row-1 == self.ss_row:
                if self.board[self.ts_row][self.ts_col] == "--":
                    if self.ss_row == 4:
                        last_move = self.game_log[-1]
                        last_ss_row = last_move[0]
                        last_ss_col = last_move[1]
                        last_ts_row = last_move[2]
                        last_ts_col = last_move[3]
                        last_start_piece = self.board[last_ss_row][last_ss_col]
                        last_target_piece = self.board[last_ts_row][last_ts_col]
                        if last_target_piece == "WP":
                            if last_ss_row - 2 == last_ts_row:
                                if last_ss_col - 1 == self.ss_col:
                                    if self.ss_row != self.ts_row:
                                        if self.ts_col -1 == self.ss_col and self.ts_row-1 == self.ss_row:
                                            start_piece = self.board[self.ss_row][self.ss_col]
                                            self.board[self.ss_row][self.ss_col] = "--"
                                            self.board[self.ts_row-1][self.ts_col] = "--"
                                            self.board[self.ts_row][self.ts_col] = start_piece
                                            self.game_log.append((self.ss_row,self.ss_col, self.ts_row,self.ts_col, self.board[self.ss_row][self.ss_col], self.board[self.ts_row][self.ts_col],"enpassant"))

                                if last_ss_col + 1 == self.ss_col:
                                    if self.ss_row != self.ts_row:
                                        if self.ts_col +1 == self.ss_col and self.ts_row-1 == self.ss_row:
                                            start_piece = self.board[self.ss_row][self.ss_col]
                                            self.board[self.ss_row][self.ss_col] = "--"
                                            self.board[self.ts_row-1][self.ts_col] = "--"
                                            self.board[self.ts_row][self.ts_col] = start_piece
                                            self.game_log.append((self.ss_row,self.ss_col, self.ts_row,self.ts_col, self.board[self.ss_row][self.ss_col], self.board[self.ts_row][self.ts_col],"enpassant"))
                elif self.board[self.ts_row][self.ts_col] != "--" and self.ss_row != self.ts_row:
                    self.make_move()

    def rook_rules(self):
        """
        directions = ((-1,0), (0,-1), (1,0), (0,1))
		enemy_color = "b" if self.white_to_move else "w"
		for d in directions:
			for i in range(1,8):
				end_row = r+d[0]*i
				end_col = c+d[1]*i
				if 0<= end_row < 8 and 0 <= end_col < 8: # check if move is on the board
					end_piece = self.board[end_row][end_col]
					if end_piece == "--":
						moves.append(Move((r,c), (end_row,end_col), self.board))
					elif end_piece[0] == enemy_color:
						moves.append(Move((r,c),(end_row,end_col), self.board))
						break
					else:
						break
				else:
					break
        """
        print("In Rook function")
        piece_color = self.selected_piece[0]
        possible_moves = []
        if self.ss_row == self.ts_row or self.ss_col == self.ts_col:
            print("legal rock move")
            if self.ss_row == self.ts_row:
                if self.ss_col < self.ts_col:
                    print("Rook move right")
                    dif = self.ts_col - self.ss_col
                    dif -= 1
                    if dif == 0:
                        if self.board[self.ts_row][self.ts_col]!= piece_color:
                            self.make_move()
                    else:
                        for i in range(dif):
                            i+=1
                            if self.board[self.ss_row][self.ss_col+i] == "--":
                                possible_moves.append(1)
                            else:
                                possible_moves.append(0)
                        if 0 in possible_moves:
                            print("Rook illegal move")
                        else:
                            self.make_move()

                elif self.ss_col > self.ts_col:
                    print("Rook move left")
                    dif = self.ss_col - self.ts_col
                    dif -= 1
                    if dif == 0:
                        if self.board[self.ts_row][self.ts_col][0]!= piece_color:
                            self.make_move()
                    else:
                        for i in range(dif):
                            i+=1
                            if self.board[self.ss_row][self.ss_col-i] == "--":
                                possible_moves.append(1)
                            else:
                                print("Rook illegal move")
                                possible_moves.append(0)
                        if 0 in possible_moves:
                            print("Rook illegal move")
                        else:
                            self.make_move()
            elif self.ss_col == self.ts_col:
                if self.ss_row > self.ts_row:
                    print("Rook move up")
                    dif = self.ss_row - self.ts_row
                    dif -= 1
                    if dif == 0:
                        if self.board[self.ts_row][self.ts_col][0]!= piece_color:
                            self.make_move()
                    else:
                        for i in range(dif):
                            i+=1
                            if self.board[self.ss_row-i][self.ss_col] == "--":
                                possible_moves.append(1)
                            else:
                                print("Rook illegal move")
                                possible_moves.append(0)

                        if 0 in possible_moves:
                            print("rock illegal move")
                            possible_moves.append(0)
                        else:
                            self.make_move()

                elif self.ss_row < self.ts_row:
                    print("rock move down")
                    dif = self.ts_row - self.ss_row
                    dif -= 1
                    if dif == 0:
                        if self.board[self.ts_row][self.ts_col] != piece_color:
                            self.make_move()
                    else:
                        for i in range(dif):
                            i+=1
                            if self.board[self.ss_row+i][self.ss_col] == "--":
                                possible_moves.append(1)
                            else:
                                print("Rook illegal move")
                                possible_moves.append(0)

                        if 0 in possible_moves:
                            print("illegal Rook move")
                            possible_moves.append(0)
                        else:
                            self.make_move()

        elif self.board[self.ts_row][self.ts_col][0] == self.board[self.ss_row][self.ss_col][0]:
            print("Rook illegal move")
        else:
            print("Rook Illegal movie")

    def bishop_rules(self):
        print("In Bishop function")
        move = ()
        possible_to_move = False
        row_dif = self.ss_row - self.ts_row
        col_dif = self.ss_col - self.ts_col
        a = row_dif
        b = col_dif
        if a <0:
            a *= -1
        if b < 0:
            b *= -1
        dif = row_dif
        move = ()
        if row_dif >0 and col_dif<0:
            move = (-1,1)
        elif row_dif <0 and col_dif <0:
            move = (1,1)
        elif row_dif >0 and col_dif>0:
            move = (-1,-1)
        elif row_dif <0 and col_dif >0:
            move = (1,-1)

        if dif <0:
            dif *= -1

		#-- 1) Filter the vertical and horizontal moves
        if a-b == 0:
            if dif == 1:
                if self.board[self.ts_row][self.ts_col][0] != self.board[self.ss_row][self.ss_col][0]:
                    self.make_move()

            elif dif > 1:
                print("Checking the squares between piece and target square")
                for i in range(dif):
                    r = self.ts_row
                    c = self.ts_col
                    r = self.ss_row + move[0] * i
                    c = self.ss_col + move[1] * i
                    print(self.board[r][c])
                    if self.board[r][c] == "--" or self.board[r][c] == self.board[self.ss_row][self.ss_col]:
                        if self.board[r][c][0] != self.board[self.ss_row][self.ss_col][0]:
                            print("possible")
                            possible_to_move = True
                    else:
                        possible_to_move = False
                        print("illegal movene ")

            if possible_to_move == True and self.board[self.ts_row][self.ts_col][0] != self.board[self.ss_row][self.ss_col][0]:
                    if possible_to_move == True:
                        self.make_move()
        else:
            print("illegal move")

    def knight_rules(self):
        print("In Knight function")
        possible_moves = [(self.ss_row+2,self.ss_col+1),(self.ss_row+2,self.ss_col-1),(self.ss_row-2,self.ss_col+1),(self.ss_row-2,self.ss_col-1),
        (self.ss_row+1,self.ss_col+2),(self.ss_row+1,self.ss_col-2),(self.ss_row-1,self.ss_col+2),(self.ss_row-1,self.ss_col-2)]
        if (self.ts_row,self.ts_col) in possible_moves:
            self.make_move()

    def queen_rules(self):
        print("In Queen function")
        self.rook_rules()
        self.bishop_rules()

    def king_rules(self):
        possible_moves = [(-1,0),(1,0),(0,-1),(0,1),(1,-1),(-1,-1),(1,1),(-1,1),]
        self.squares_to_check = []
        print("In King function")
        kings_color = self.selected_piece[0]
        #-- Castling move
        #-- trying to short casle
        dif = self.ss_col - self.ts_col
        print(dif)
        if dif == -2:
            print("King castle")
            if kings_color == "W" and self.board[7][7] == "WR":
                self.attempt_to_short_castle = True
                self.squares_to_check.append((self.ss_row, self.ss_col+1))
                self.squares_to_check.append((self.ss_row, self.ss_col+2))
                print(self.squares_to_check)
                self.search_for_check()

            elif kings_color == "B" and self.board[0][7] == "BR":
                self.attempt_to_short_castle = True
                self.squares_to_check.append((self.ss_row, self.ss_col+1))
                self.squares_to_check.append((self.ss_row, self.ss_col+2))
                print(self.squares_to_check)
                self.search_for_check()
        #-- Trying to long casle
        elif dif == 2:
            print("Queen castle")
            if kings_color == "W" and self.board[7][0] == "WR":
                self.attempt_to_long_castle = True
                self.squares_to_check.append((self.ss_row, self.ss_col-1))
                self.squares_to_check.append((self.ss_row, self.ss_col-2))
                self.search_for_check()

            elif kings_color == "B" and self.board[0][0] == "BR":
                self.attempt_to_long_castle = True
                self.squares_to_check.append((self.ss_row, self.ss_col-1))
                self.squares_to_check.append((self.ss_row, self.ss_col-2))
                self.search_for_check()

        else: #-- check for normal move
            move = (self.ss_row - self.ts_row, self.ss_col - self.ts_col)
            if move in possible_moves:
                square = self.ts_row, self.ts_col
                self.squares_to_check.append(square)
                self.search_for_check()
            else:
                print("Illegal King move")

        print("***************************")
        print("back to king rules")
        with open("board_copy.txt", "r") as file:
            new_board = [[col for col in row.split()] for row in file]
        self.board = new_board

        time.sleep(0.05)
        engine_tick.play()
        if 1 not in self.check_switches and self.attempt_to_short_castle == True and dif == -2:
            print("Short castle")
            if self.selected_piece[0] == "W":
                move = [move for move in self.game_log if "WK" in move]
                print(move)
                if self.WK_short_castle == True and self.white_castle == True:
                    target_piece = self.target_piece
                    piece = self.selected_piece
                    self.board[self.ts_row][self.ts_col] = piece
                    self.board[self.ss_row][self.ss_col] = "--"
                    self.board[7][7] = "--"
                    self.board[7][5] = "WR"
                    self.print_board()
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece,"castle"))
                    self.game_state = []

            elif self.selected_piece[0] == "B":
                if self.BK_short_castle == True and self.black_castle == True:
                    target_piece = self.target_piece
                    piece = self.selected_piece
                    self.board[self.ts_row][self.ts_col] = piece
                    self.board[self.ss_row][self.ss_col] = "--"
                    self.board[0][7] = "--"
                    self.board[0][5] = "BR"
                    self.print_board()
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece,"castle"))
                    self.game_state = []

        elif 1 not in self.check_switches and self.attempt_to_long_castle == True and dif == 2:
            print("Long castle")
            if self.selected_piece[0] == "W":
                if self.WK_long_castle == True:
                    target_piece = self.target_piece
                    piece = self.selected_piece
                    self.board[self.ts_row][self.ts_col] = piece
                    self.board[self.ss_row][self.ss_col] = "--"
                    self.board[7][3] = "WR"
                    self.board[7][0] = "--"
                    self.print_board()
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece,"castle"))
                    self.game_state = []

            elif self.selected_piece[0] == "B":
                if self.BK_long_castle == True:
                    target_piece = self.target_piece
                    piece = self.selected_piece
                    self.board[self.ts_row][self.ts_col] = piece
                    self.board[self.ss_row][self.ss_col] = "--"
                    self.board[0][0] = "--"
                    self.board[0][3] = "BR"
                    self.print_board()
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece,"castle"))
                    self.game_state = []

        elif 1 not in self.check_switches:
            move = (self.ss_row - self.ts_row, self.ss_col - self.ts_col)
            if move in possible_moves:
                self.game_state = []
                self.make_move()
        print("End of the king rules function")

    def search_for_check(self):
        self.check_switches = []
        """
        Spot is the target square that going to be checked
        can be more than one.
        """
        print("in search for check function")
        rock_possible_moves = []
        color = ""
        if self.white_turn:
            color = "B"
        else:
            color = "W"
        """
        Making a copy of actual game
        """
        self.game_state = self.board

        piece_color = color
        for row in self.game_state:
            r = self.game_state.index(row)
            for col in row:
                c = row.index(col)
                #-- rook
                if self.game_state[r][c] == (color+"R"):
                    for square in self.squares_to_check:
                        print("Square to check: ", square)
                        time.sleep(0.05)
                        engine_tick.play()
                        print("Rook's positions")
                        print(r,c)
                        time.sleep(0.05)
                        engine_tick.play()
                        #-- Algorithm starts here
                        if r == square[0] or c == square[1]:
                            if r == square[0]:
                                #-- left and right check
                                if c < square[1]:
                                    print("Rook move right") #-- working
                                    dif = square[1] - c
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c+i] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                rock_possible_moves.append(0)
                                            if 0 in rock_possible_moves:
                                                print("Illegal rook move")
                                                self.game_state[r][c] = "--"
                                            else:
                                                self.check_switches.append(1)

                                elif c > square[1]:
                                    print("Rook move left") #working
                                    dif = c - square[1]
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c-i] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                print("Rook illegal move")

                                                self.game_state[r][c] = "--"
                                                rock_possible_moves.append(0)
                                            if 0 in rock_possible_moves:
                                                print("Rook illegal move")
                                                self.check_switches
                                                self.game_state[r][c] = "--"
                                            else:
                                                self.check_switches.append(1)

                            elif c == square[1]:
                                if r > square[0]:
                                    print("Rook move up")
                                    dif = r - square[0]
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r-i][c] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                self.game_state[r][c] = "--"
                                                rock_possible_moves.append(0)
                                        if 0 in rock_possible_moves:
                                            print("Illegal rook move")
                                            self.game_state[r][c] = "--"
                                        else:
                                            self.check_switches.append(1)

                                elif r < square[0]:
                                    print("rock move down")
                                    dif = square[0] - r
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r+i][c] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                print("illegal Rook move")
                                                self.game_state[r][c] = "--"
                                                rock_possible_moves.append(0)
                                        if 0 in rock_possible_moves:
                                            print("illegal Rook move")
                                            self.game_state[r][c] = "--"
                                        else:
                                            self.check_switches.append(1)

                        elif self.game_state[square[0]][square[1]][0] == self.game_state[r][c][0]:
                            print("Rook illegal move")
                            self.game_state[r][c] = "--"
                        else:
                            print("Rook Illegal movie")
                            self.game_state[r][c] = "--"
                        time.sleep(0.05)
                        engine_tick.play()


                if self.game_state[r][c] == (color+"B"):
                    for square in self.squares_to_check:
                        print("check for bishops")
                        print(color)
                        print(self.check_switches)
                        time.sleep(0.05)
                        engine_tick.play()
                        possible_to_move = False
                        row_dif = r - square[0]
                        col_dif = c - square[1]
                        print("****** Target")
                        print(self.ts_row, self.ts_col)
                        print("****** Square")
                        print(square)
                        time.sleep(0.05)
                        engine_tick.play()
                        a = row_dif
                        b = col_dif
                        if a <0:
                            a *= -1
                        if b < 0:
                            b *= -1
                        dif = row_dif
                        move = ()
                        if row_dif >0 and col_dif<0:
                            move = (-1,1)
                        elif row_dif <0 and col_dif <0:
                            move = (1,1)
                        elif row_dif >0 and col_dif>0:
                            move = (-1,-1)
                        elif row_dif <0 and col_dif >0:
                            move = (1,-1)

                        if dif <0:
                            dif *= -1
    					#-- 1) Filter the vertical and horizontal moves
                        if a-b == 0:
                            print(square[1], c, square[0], r)
                            print(a,b)
                        #--2) Keeps the bishop on fixed color diagonals
                            system("cls")
                            print("dif and move")
                            print(dif)
                            if dif == 1:
                                if self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    self.check_switches.append(1)
                            elif dif > 1:
                                print("Checking the squares between piece and target square")
                                for i in range(dif):
                                    temp_r = square[0]
                                    temp_c = square[1]
                                    temp_r = r + move[0] * i
                                    temp_c = c + move[1] * i
                                    if (temp_r,temp_c) in self.game_state:
                                        print(self.game_state[temp_r][temp_c])
                                    else:
                                        print("Error")
                                        print(r,c)
                                        print(square[0],square[1])
                                    if self.game_state[temp_r][temp_c] == "--" or self.game_state[temp_r][temp_c] == self.game_state[r][c]:
                                        if self.game_state[temp_r][temp_c][0] != self.game_state[r][c][0]:
                                            print("possible")
                                            possible_to_move = True

                                    else:
                                        possible_to_move = False
                                        self.game_state[r][c] = '--'
                            if possible_to_move == True and self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    if possible_to_move == True:
                                        self.check_switches.append(1)

                        else:
                            self.game_state[r][c] = '--'
                            pass

                if  self.game_state[r][c] == (color+"N"):
                        print("check for knights")
                        for square in self.squares_to_check:
                            possible_moves = [(r+2,c+1),(r+2,c-1),(r-2,c+1),(r-2,c-1),
                            (r+1,c+2),(r+1,c-2),(r-1,c+2),(r-1,c-2)]
                            if (square[0],square[1]) in possible_moves:
                                self.check_switches.append(1)

                if self.game_state[r][c] == (color+"Q"):
                    print("Check for queen")
                    for square in self.squares_to_check:
                        print("Square in beginning of the algorithm")
                        print("Square: ", square)
                        time.sleep(0.05)
                        engine_tick.play()
                        piece_color = self.game_state[r][c][0]
                        print("Rooks are in these positions")
                        print(r,c)

                        #-- Algorithm starts here
                        possible_moves = []
                        if r == self.ts_row or c == self.ts_col:
                            # self.game_state[r][c] = "--"
                            if r == self.ts_row:
                                if c < self.ts_col:
                                    print("Rook move to right")
                                    dif = self.ts_col - c
                                    dif -= 1
                                    if dif >= 1:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c+i] == "--":
                                                possible_moves.append(1)
                                            else:
                                                possible_moves.append(0)
                                    if 0 in possible_moves:
                                        print("Rook illegal move")
                                        # self.game_state[r][c] = "--"
                                    else:
                                        self.check_switches.append(1)
                                elif c > self.ts_col:
                                    print("Rook move to left")
                                    dif = c - self.ts_col
                                    dif -= 1
                                    if dif >= 1:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c-i] == "--":
                                                possible_moves.append(1)
                                            else:
                                                print("Rook illegal move")
                                                # self.game_state[r][c] = "--"
                                                possible_moves.append(0)
                                    if 0 in possible_moves:
                                        print("Rook illegal move")
                                        # self.game_state[r][c] = "--"
                                    else:
                                        self.check_switches.append(1)
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                            elif c == self.ts_col:
                                if r > self.ts_row:
                                    print("Rook move to up")
                                    dif = r - self.ts_row
                                    dif -= 1
                                    if dif >= 1:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r-i][c] == "--":
                                                possible_moves.append(1)
                                            else:
                                                print("Rook illegal move")
                                                # self.game_state[r][c] = "--"
                                                possible_moves.append(0)
                                    if 0 in possible_moves:
                                        print("rock illegal move")
                                        # self.game_state[r][c] = "--"
                                    else:
                                        self.check_switches.append(1)
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                elif r < self.ts_row:
                                    print("rock move down")
                                    dif = self.ts_row - r
                                    dif -= 1
                                    if dif >= 1:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r+i][c] == "--":
                                                possible_moves.append(1)
                                            else:
                                                print("illegal Rook move")
                                                # self.game_state[r][c] = "--"
                                                possible_moves.append(0)
                                    if 0 in possible_moves:
                                        print("illegal Rook move")
                                        # self.game_state[r][c] = "--"
                                    else:
                                        self.check_switches.append(1)
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col] != piece_color:
                                            self.check_switches.append(1)
                        elif self.game_state[self.ts_row][self.ts_col][0] == self.game_state[r][c][0]:
                            print("Rook illegal move")
                            # self.game_state[r][c] = "--"
                        else:
                            print("Rook Illegal movie")
                            # self.game_state[r][c] = "--"


                        possible_to_move = False
                        row_dif = r - square[0]
                        col_dif = c - square[1]
                        print("****** Target")
                        print(self.ts_row, self.ts_col)
                        print("****** Square")
                        print(square)
                        time.sleep(0.05)
                        engine_tick.play()
                        a = row_dif
                        b = col_dif
                        if a <0:
                            a *= -1
                        if b < 0:
                            b *= -1
                        dif = row_dif
                        move = ()
                        if row_dif >0 and col_dif<0:
                            move = (-1,1)
                        elif row_dif <0 and col_dif <0:
                            move = (1,1)
                        elif row_dif >0 and col_dif>0:
                            move = (-1,-1)
                        elif row_dif <0 and col_dif >0:
                            move = (1,-1)

                        if dif <0:
                            dif *= -1
    					#-- 1) Filter the vertical and horizontal moves
                        if a-b == 0:
                            print(square[1], c, square[0], r)
                            print(a,b)
                        #--2) Keeps the bishop on fixed color diagonals
                            system("cls")
                            print("dif and move")
                            print(dif)
                            if dif == 1:
                                if self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    self.check_switches.append(1)
                            elif dif > 1:
                                print("Checking the squares between piece and target square")
                                for i in range(dif):
                                    temp_r = square[0]
                                    temp_c = square[1]
                                    temp_r = r + move[0] * i
                                    temp_c = c + move[1] * i
                                    if (temp_r,temp_c) in self.game_state:
                                        print(self.game_state[temp_r][temp_c])
                                    else:
                                        print("Error")
                                        print(r,c)
                                        print(square[0],square[1])
                                    if self.game_state[temp_r][temp_c] == "--" or self.game_state[temp_r][temp_c] == self.game_state[r][c]:
                                        if self.game_state[temp_r][temp_c][0] != self.game_state[r][c][0]:
                                            print("possible")
                                            possible_to_move = True

                                    else:
                                        possible_to_move = False
                                        self.game_state[r][c] = '--'
                            if possible_to_move == True and self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    if possible_to_move == True:
                                        self.check_switches.append(1)

                        else:
                            self.game_state[r][c] = '--'
                            pass

                if self.game_state[r][c] == (color+"P"):
                    print("Check for pawns")
                    for square in self.squares_to_check:
                        if piece_color == "W":
                            if square[0]+1 ==r:
                                if c-1 == square[1] or c+1 == square[1]:
                                    self.check_switches.append(1)
                                else:
                                    self.game_state[r][c] = "--"

                        elif piece_color == "B":
                            if square[0]-1 == r:
                                if c-1 == square[1] or c+1 == square[1]:
                                    print("C and SQUARE[1]")
                                    print(c,square[1])
                                    self.check_switches.append(1)
                                else:
                                    self.game_state[r][c] = "--"

                if self.game_state[r][c] == (color+"K"):
                    for square in self.squares_to_check:
                        possible_king_moves = [(-1,0),(1,0),(0,-1),(0,1),(1,-1),(-1,-1),(1,1),(-1,1)]
                        move = (r - square[0], c - square[1])
                        if move in possible_king_moves:
                            self.check_switches.append(1)

        print("End of the check function")
        print(self.check_switches)

    def game_state_check(self):
        print("In game state check function")
        time.sleep(0.05)
        wk_pos = self.wk_pos
        bk_pos = self.bk_pos

        self.game_state = self.board
        ss_row = self.ss_row
        ss_col = self.ss_col
        ts_row = self.ts_row
        ts_col = self.ts_col

        piece = self.game_state[ss_row][ss_col]
        target = self.game_state[ts_row][ts_col]
        self.game_state[ss_row][ss_col] = "--"
        self.game_state[ts_row][ts_col] = piece

        self.check_switches = []
        self.squares_to_check = []

        for row in self.board:
            r = self.game_state.index(row)
            for col in row:
                c = row.index(col)
                if self.game_state[r][c] =="BK":
                    bk_pos = (r,c)

                elif self.game_state[r][c] == "WK":
                    wk_pos = (r,c)
        """
        Spot is the target square that going to be checked
        can be more than one.
        """
        print("In Game state check function")

        color = ""
        if self.white_turn:
            color = "B"
            self.squares_to_check.append(wk_pos)

        else:
            color = "W"
            self.squares_to_check.append(bk_pos)
        print(self.squares_to_check)
        time.sleep(0.05)
        """
        Making a copy of actual game
        """
        piece_color = color
        print("Color to for check: ", piece_color)
        time.sleep(0.05)
        for row in self.game_state:
            r = self.game_state.index(row)
            for col in row:
                c = row.index(col)
                #-- rook
                rock_possible_moves = []
                if self.game_state[r][c] == (color+"R"):
                    for square in self.squares_to_check:
                        print("Square to check: ", square)
                        time.sleep(0.05)
                        engine_tick.play()
                        print("Rook's positions")
                        print(r,c)
                        time.sleep(0.05)
                        engine_tick.play()
                        #-- Algorithm starts here
                        if r == square[0] or c == square[1]:
                            if r == square[0]:
                                #-- left and right check
                                if c < square[1]:
                                    print("Rook move right") #-- working
                                    dif = square[1] - c
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c+i] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                rock_possible_moves.append(0)
                                            if 0 in rock_possible_moves:
                                                print("Illegal rook move")
                                                self.game_state[r][c] = "--"
                                            else:
                                                self.check_switches.append(1)

                                elif c > square[1]:
                                    print("Rook move left") #working
                                    dif = c - square[1]
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c-i] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                print("Rook illegal move")

                                                self.game_state[r][c] = "--"
                                                rock_possible_moves.append(0)
                                            if 0 in rock_possible_moves:
                                                print("Rook illegal move")
                                                self.check_switches
                                                self.game_state[r][c] = "--"
                                            else:
                                                self.check_switches.append(1)

                            elif c == square[1]:
                                if r > square[0]:
                                    print("Rook move up")
                                    dif = r - square[0]
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r-i][c] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                self.game_state[r][c] = "--"
                                                rock_possible_moves.append(0)
                                        if 0 in rock_possible_moves:
                                            print("Illegal rook move")
                                            self.game_state[r][c] = "--"
                                        else:
                                            self.check_switches.append(1)

                                elif r < square[0]:
                                    print("rock move down")
                                    dif = square[0] - r
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r+i][c] == "--":
                                                rock_possible_moves.append(1)
                                            else:
                                                print("illegal Rook move")
                                                self.game_state[r][c] = "--"
                                                rock_possible_moves.append(0)
                                        if 0 in rock_possible_moves:
                                            print("illegal Rook move")
                                            self.game_state[r][c] = "--"
                                        else:
                                            self.check_switches.append(1)

                        elif self.game_state[square[0]][square[1]][0] == self.game_state[r][c][0]:
                            print("Rook illegal move")
                            self.game_state[r][c] = "--"
                        else:
                            print("Rook Illegal movie")
                            self.game_state[r][c] = "--"
                        time.sleep(0.05)
                        engine_tick.play()

                    print("After rook check: ", self.check_switches)
                    time.sleep(0.05)


                if self.game_state[r][c] == (color+"B"):
                    for square in self.squares_to_check:
                        print("check for bishops")
                        print(color)
                        print(self.check_switches)
                        time.sleep(0.05)
                        engine_tick.play()
                        bishop_possible_to_move = False
                        row_dif = r - square[0]
                        col_dif = c - square[1]
                        print("****** Target")
                        print(self.ts_row, self.ts_col)
                        print("****** Square")
                        print(square)
                        time.sleep(0.05)
                        engine_tick.play()
                        a = row_dif
                        b = col_dif
                        if a <0:
                            a *= -1
                        if b < 0:
                            b *= -1
                        dif = row_dif
                        move = ()
                        if row_dif >0 and col_dif<0:
                            move = (-1,1)
                        elif row_dif <0 and col_dif <0:
                            move = (1,1)
                        elif row_dif >0 and col_dif>0:
                            move = (-1,-1)
                        elif row_dif <0 and col_dif >0:
                            move = (1,-1)

                        if dif <0:
                            dif *= -1
    					#-- 1) Filter the vertical and horizontal moves
                        if a-b == 0:
                            print(square[1], c, square[0], r)
                            print(a,b)
                        #--2) Keeps the bishop on fixed color diagonals
                            system("cls")
                            print("dif and move")
                            print(dif)
                            if dif == 1:
                                if self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    self.check_switches.append(1)
                            elif dif > 1:
                                print("Checking the squares between piece and target square")
                                for i in range(dif):
                                    temp_r = square[0]
                                    temp_c = square[1]
                                    temp_r = r + move[0] * i
                                    temp_c = c + move[1] * i
                                    if (temp_r,temp_c) in self.game_state:
                                        print(self.game_state[temp_r][temp_c])
                                    else:
                                        print("Error")
                                        print(r,c)
                                        print(square[0],square[1])
                                    if self.game_state[temp_r][temp_c] == "--" or self.game_state[temp_r][temp_c] == self.game_state[r][c]:
                                        if self.game_state[temp_r][temp_c][0] != self.game_state[r][c][0]:
                                            print("possible")
                                            bishop_possible_to_move = True

                                    else:
                                        bishop_possible_to_move = False
                                        self.game_state[r][c] = '--'
                            if bishop_possible_to_move == True and self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    if bishop_possible_to_move == True:
                                        self.check_switches.append(1)

                        else:
                            self.game_state[r][c] = '--'
                            pass
                    print("After bishop check: ", self.check_switches)
                    time.sleep(0.05)

                if  self.game_state[r][c] == (color+"N"):
                        print("check for knights")
                        for square in self.squares_to_check:
                            possible_moves = [(r+2,c+1),(r+2,c-1),(r-2,c+1),(r-2,c-1),
                            (r+1,c+2),(r+1,c-2),(r-1,c+2),(r-1,c-2)]
                            if (square[0],square[1]) in possible_moves:
                                self.check_switches.append(1)

                        print("After knight check: ", self.check_switches)
                        time.sleep(0.05)

                if self.game_state[r][c] == (color+"Q"):
                    print("Check for queen")
                    for square in self.squares_to_check:
                        print("Square in beginning of the algorithm")
                        print("Square: ", square)
                        time.sleep(0.05)
                        engine_tick.play()
                        piece_color = self.game_state[r][c][0]
                        print("Rooks are in these positions")
                        print(r,c)

                        #-- Algorithm starts here
                        queen_possible_moves = []
                        if r == square[0] or c == square[1]:
                            if r == square[0]:
                                #-- left and right check
                                if c < square[1]:
                                    print("Rook move right") #-- working
                                    dif = square[1] - c
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c+i] == "--":
                                                queen_possible_moves.append(1)
                                            else:
                                                queen_possible_moves.append(0)
                                            if 0 in queen_possible_moves:
                                                print("Illegal rook move")
                                                self.game_state[r][c] = "--"
                                            else:
                                                self.check_switches.append(1)

                                elif c > square[1]:
                                    print("Rook move left") #working
                                    dif = c - square[1]
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r][c-i] == "--":
                                                queen_possible_moves.append(1)
                                            else:
                                                print("Rook illegal move")

                                                self.game_state[r][c] = "--"
                                                queen_possible_moves.append(0)
                                            if 0 in queen_possible_moves:
                                                print("Rook illegal move")
                                                self.check_switches
                                                self.game_state[r][c] = "--"
                                            else:
                                                self.check_switches.append(1)

                            elif c == square[1]:
                                if r > square[0]:
                                    print("Rook move up")
                                    dif = r - square[0]
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r-i][c] == "--":
                                                queen_possible_moves.append(1)
                                            else:
                                                self.game_state[r][c] = "--"
                                                queen_possible_moves.append(0)
                                        if 0 in queen_possible_moves:
                                            print("Illegal rook move")
                                            self.game_state[r][c] = "--"
                                        else:
                                            self.check_switches.append(1)

                                elif r < square[0]:
                                    print("rock move down")
                                    dif = square[0] - r
                                    dif -= 1
                                    if dif == 0:
                                        if self.game_state[self.ts_row][self.ts_col][0]!= piece_color:
                                            self.check_switches.append(1)
                                    else:
                                        for i in range(dif):
                                            i+=1
                                            if self.game_state[r+i][c] == "--":
                                                queen_possible_moves.append(1)
                                            else:
                                                print("illegal Rook move")
                                                self.game_state[r][c] = "--"
                                                queen_possible_moves.append(0)
                                        if 0 in queen_possible_moves:
                                            print("illegal Rook move")
                                            self.game_state[r][c] = "--"
                                        else:
                                            self.check_switches.append(1)

                        elif self.game_state[square[0]][square[1]][0] == self.game_state[r][c][0]:
                            print("Rook illegal move")
                            self.game_state[r][c] = "--"
                        else:
                            print("Rook Illegal movie")
                            self.game_state[r][c] = "--"
                        time.sleep(0.05)
                        engine_tick.play()

                        print("After rook part of the queen function: ", self.check_switches)
                        time.sleep(0.5)

                        #-- Diagonal algorithm
                        queen_possible_to_move = False
                        row_dif = r - square[0]
                        col_dif = c - square[1]
                        print("****** Target")
                        print(ts_row, ts_col)
                        print("****** Square")
                        print(square)
                        time.sleep(0.05)
                        engine_tick.play()
                        a = row_dif
                        b = col_dif
                        if a <0:
                            a *= -1
                        if b < 0:
                            b *= -1
                        dif = row_dif
                        move = ()
                        if row_dif >0 and col_dif<0:
                            move = (-1,1)
                        elif row_dif <0 and col_dif <0:
                            move = (1,1)
                        elif row_dif >0 and col_dif>0:
                            move = (-1,-1)
                        elif row_dif <0 and col_dif >0:
                            move = (1,-1)

                        if dif <0:
                            dif *= -1
    					#-- 1) Filter the vertical and horizontal moves
                        if a-b == 0:
                            print(square[1], c, square[0], r)
                            print(a,b)
                        #--2) Keeps the bishop on fixed color diagonals
                            system("cls")
                            print("dif and move")
                            print(dif)
                            if dif == 1:
                                if self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                    self.check_switches.append(1)
                            elif dif > 1:
                                print("Checking the squares between piece and target square")
                                for i in range(dif):
                                    temp_r = square[0]
                                    temp_c = square[1]
                                    temp_r = r + move[0] * i
                                    temp_c = c + move[1] * i
                                    if (temp_r,temp_c) in self.game_state:
                                        print(self.game_state[temp_r][temp_c])
                                    else:
                                        print("Error")
                                        print(r,c)
                                        print(square[0],square[1])
                                    if self.game_state[temp_r][temp_c] == "--" or self.game_state[temp_r][temp_c] == self.game_state[r][c]:
                                        if self.game_state[temp_r][temp_c][0] != self.game_state[r][c][0]:
                                            print("possible")
                                            queen_possible_to_move = True

                                    else:
                                        queen_possible_to_move = False
                                        self.game_state[r][c] = '--'
                            if queen_possible_to_move == True and self.game_state[square[0]][square[1]][0] != self.game_state[r][c][0]:
                                self.check_switches.append(1)

                        else:
                            self.game_state[r][c] = '--'
                            pass
                    print("After queen check: ", self.check_switches)
                    time.sleep(0.05)

                if self.game_state[r][c] == (color+"P"):
                    print("Check for pawns")
                    print("Piece color: ", piece_color)
                    for square in self.squares_to_check:
                        if piece_color == "W":
                            if square[0]+1 ==r:
                                if c-1 == square[1] or c+1 == square[1]:
                                    self.check_switches.append(1)
                                else:
                                    self.game_state[r][c] = "--"

                        elif piece_color == "B":
                            if square[0]-1 == r:
                                if c-1 == square[1] or c+1 == square[1]:
                                    print("C and SQUARE[1]")
                                    print(c,square[1])
                                    self.check_switches.append(1)
                                else:
                                    self.game_state[r][c] = "--"
                    print("After Pawn check: ", self.check_switches)
                    time.sleep(0.05)


        print("End of the game state check: ",self.check_switches)
        time.sleep(0.05)

    def make_move(self):
        print("*****************************")
        print("Calling game update function for castling rules")
        self.game_update()
        print("White king castle: ", self.white_castle)
        print("Black king castle: ", self.black_castle)

        print()
        print("In make move function")
        time.sleep(0.05)
        print("testing new function")
        self.game_state_check()
        #-- problem ------------
        with open("board_copy.txt", "r") as file:
            new_board = [[col for col in row.split()] for row in file]
        self.board = new_board
        if self.board[self.ss_row][self.ss_col][1] != "K" and 1 in self.check_switches:
            print("King is in check")

        if self.board[self.ss_row][self.ss_col][1] != "K" and 1 not in self.check_switches:

                print("Back to make a move function")
                time.sleep(0.05)

                target_piece = self.target_piece
                piece = self.selected_piece
                self.board[self.ts_row][self.ts_col] = piece
                self.board[self.ss_row][self.ss_col] = "--"

                if piece == "WP" and self.ts_row == 0:
                    self.board[self.ts_row][self.ts_col] = "WQ"
                    self.board[self.ts_row+1][self.ts_col] = "--"
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece, "pawn_promotion"))

                elif piece == "BP" and self.ts_row == 7:
                    self.board[self.ts_row][self.ts_col] = "BQ"
                    self.board[self.ts_row-1][self.ts_col] = "--"
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece, "pawn_promotion"))

                else:
                    self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece))
                    print("WK SHORT: ",self.WK_short_castle)
                    print("WK LONG: ",self.WK_long_castle)
                    print("BK SHORT: ", self.BK_short_castle)
                    print("BK LONG: ", self.BK_long_castle)
                    print("len game log: ", len(self.game_log))
                    print("\n")
                    self.print_board()
                    time.sleep(0.05)
        if self.board[self.ss_row][self.ss_col][1] == "K":
            target_piece = self.target_piece
            piece = self.selected_piece
            self.board[self.ts_row][self.ts_col] = piece
            self.board[self.ss_row][self.ss_col] = "--"
            self.game_log.append((self.ss_row,self.ss_col,self.ts_row,self.ts_col, self.board[self.ts_row][self.ts_col], self.target_piece))


    def undo_move(self):
        system("cls")
        print("In undo function")

        if len(self.game_log) != 0:
            print("in undo function")
            last_move = self.game_log[-1]
            self.game_log.pop()
            start_piece = last_move[4]
            target_piece = last_move[5]
            ss_row = last_move[0]
            ss_col = last_move[1]
            ts_row = last_move[2]
            ts_col = last_move[3]

            if last_move[-1] == "pawn_promotion":
                    print(last_move)
                    if start_piece[0] == "W":
                        self.board[ss_row][ss_col] = "WP"
                        self.board[ts_row][ts_col] = "--"
                    elif start_piece[0] == "B":
                        self.board[ss_row][ss_col] = "BP"
                        self.board[ts_row][ts_col] = "--"

            if last_move[-1] == "enpassant":
                print("enpassant move")
                time.sleep(0.05)
                old_target_piece = last_move[4]
                self.board[ss_row][ss_col] = target_piece
                self.board[ts_row][ts_col] = old_target_piece
                if target_piece == "WP":
                    self.board[ss_row][ss_col] = target_piece
                    self.board[ts_row+1][ts_col] = "BP"
                if target_piece == "BP":
                    self.board[ss_row][ss_col] = target_piece
                    self.board[ts_row-1][ts_col] = "WP"

            if last_move[-1] == "castle":
                print("last move was castle")
                time.sleep(0.05)
                if start_piece == "WK":
                    self.board[7][4] = "WK"
                    if self.ts_col == 6:
                        self.board[7][5] = "--"
                        self.board[7][6] = "--"
                        self.board[7][7] = "WR"
                        self.WK_short_castle = True
                        print()
                        print("board state at the end of the undo for castling")
                        self.print_board()
                        print("Len of the game log: ", len(self.game_log))
                        print()

                    elif self.ts_col == 2:
                        self.board[7][0] = "WR"
                        self.board[7][2] = "--"
                        self.board[7][3] = "--"
                        self.WK_long_castle = True
                        print()
                        print("board state at the end of the undo for castling")
                        self.print_board()
                        print("Len of the game log: ", len(self.game_log))
                        print()

                elif start_piece == "BK":
                    self.board[0][4] = "BK"
                    if ts_col == 6:
                        self.board[0][6] = "--"
                        self.board[0][5] = "--"
                        self.board[0][7] = "BR"
                        self.BK_short_castle = True
                        print()
                        print("board state at the end of the undo for castling")
                        self.print_board()
                        print("Len of the game log: ", len(self.game_log))

                    elif ts_col == 2:
                         self.board[ts_row][ts_col] == "--"
                         self.board[0][2] = "--"
                         self.board[0][3] = "--"
                         self.board[0][0] = "BR"
                         self.BK_long_castle = True
                         print()
                         print("board state at the end of the undo for castling")
                         self.print_board()
                         print("Len of the game log: ", len(self.game_log))


            if len(last_move) == 6:
                self.board[ss_row][ss_col] = start_piece
                self.board[ts_row][ts_col] = target_piece

        elif len(self.game_log)<= 0:
            print("no more move to return \n")

        # with open("board_copy.txt", 'w') as file:
        print()
        self.print_board()

    #-- Interfac related functions
    def print_board(self):
        print('\n'.join(map(''.join, self.board)))
    def print_search_table(self):
        print('\n'.join(map(''.join, self.search_table)))

    def draw_board(self):
        colors = [pygame.Color("#ebe9d3"), pygame.Color("#635014")]
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                color=colors[((row+col)%2)]
                pygame.draw.rect(screen, color, pygame.Rect(col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE,TILE_SIZE))

    def draw_pieces(self, board):
        #-- Resseting pygame container
        engine.all_pieces = pygame.sprite.Group()
        y = 0
        for row in board:
          x = 0
          for piece in row:
            if piece == "WP":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, white_pawn)
              engine.all_pieces.add(piece)
            if piece == "BP":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, black_pawn)
              engine.all_pieces.add(piece)
            if piece == "WR":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, white_rock)
              engine.all_pieces.add(piece)
            if piece == "BR":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, black_rock)
              engine.all_pieces.add(piece)
            if piece == "WN":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, white_knight)
              engine.all_pieces.add(piece)
            if piece == "BN":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, black_knight)
              engine.all_pieces.add(piece)
            if piece == "WB":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, white_bishop)
              engine.all_pieces.add(piece)
            if piece == "BB":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, black_bishop)
              engine.all_pieces.add(piece)
            if piece == "WQ":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, white_queen)
              engine.all_pieces.add(piece)
            if piece == "BQ":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, black_queen)
              engine.all_pieces.add(piece)
            if piece == "WK":
              piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, white_king)
              engine.all_pieces.add(piece)
            if piece == "BK":
               piece = Piece(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE,TILE_SIZE, black_king)
               engine.all_pieces.add(piece)
            x+=1
          y+=1

if __name__ == "__main__":
    engine = Engine()

    running = True
    while running:
        cursor_position = pygame.mouse.get_pos()
        left_click = False
        right_click = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if len(engine.move) == 2:
                        engine.undo_move()
                    else:
                        engine.move = []

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(engine.game_log) == 0 or len(engine.game_log) % 2 == 0:
                        engine.white_turn = True
                        print("White turn")
                    else:
                        engine.white_turn = False
                        print("Black turn")
                    left_click = True
                    row = cursor_position[1] // TILE_SIZE
                    col = cursor_position[0] // TILE_SIZE
                    if len(engine.move) == 2:
                        engine.move = []
                    if cursor_position[0] >= 0 and cursor_position[0] <= 510 and cursor_position[1] >= 0 and cursor_position[1] <=510:
                        if len(engine.move) == 0:
                            engine.selected_piece = board[row][col]
                            #-- Check for turn
                            if engine.white_turn == True and engine.selected_piece[0] == "W":
                                if board[row][col] != "--":
                                    engine.start_square = (row,col)
                                    print("Start square: ", engine.start_square)
                                    engine.move.append(engine.start_square)
                                    engine.selected_piece = board[row][col]
                                    print("Selected piece; ", engine.selected_piece)
                                else:
                                    print("Reseting the move")
                                    engine.move = []
                            elif engine.white_turn == False and engine.selected_piece[0] == "B":
                                if board[row][col] != "--":
                                    engine.start_square = (row,col)
                                    print("Start square: ", engine.start_square)
                                    engine.move.append(engine.start_square)
                                    engine.selected_piece = board[row][col]
                                    print("Selected piece; ", engine.selected_piece)
                                else:
                                    print("reseting the move")
                                    engine.move = []
                            else:
                                print("Wrong turn, resetting the move")
                                engine.move = []
                        elif len(engine.move) == 1:
                            pick.play()
                            print("len log: ", len(engine.game_log))
                            engine.target_square = (row,col)
                            engine.target_piece = board[row][col]
                            print("Target square", engine.target_square)
                            print("Target piece: ", engine.target_piece)
                            #-- data check
                            if engine.target_square != engine.start_square and engine.selected_piece[0] != engine.target_piece[0]:
                                engine.move.append(engine.target_square)
                                engine.ss_row = engine.start_square[0]
                                engine.ss_col = engine.start_square[1]
                                engine.ts_row = engine.target_square[0]
                                engine.ts_col = engine.target_square[1]

                                engine.check_log = []

                                #-- calling the related functions
                                if engine.selected_piece[1] == "P":
                                    with open("board_copy.txt", 'w') as file:
                                        file.writelines('\t'.join(str(col) for col in row) + '\n' for row in engine.board)
                                    engine.pawn_rules()
                                elif engine.selected_piece[1] == "R":
                                    with open("board_copy.txt", 'w') as file:
                                        file.writelines('\t'.join(str(col) for col in row) + '\n' for row in engine.board)
                                    engine.rook_rules()
                                elif engine.selected_piece[1] == "N":
                                    with open("board_copy.txt", 'w') as file:
                                        file.writelines('\t'.join(str(col) for col in row) + '\n' for row in engine.board)
                                    engine.knight_rules()
                                elif engine.selected_piece[1] == "B":
                                    with open("board_copy.txt", 'w') as file:
                                        file.writelines('\t'.join(str(col) for col in row) + '\n' for row in engine.board)
                                    engine.bishop_rules()
                                elif engine.selected_piece[1] == "Q":
                                    with open("board_copy.txt", 'w') as file:
                                        file.writelines('\t'.join(str(col) for col in row) + '\n' for row in engine.board)
                                    engine.queen_rules()
                                elif engine.selected_piece[1] == "K":
                                    with open("board_copy.txt", 'w') as file:
                                        file.writelines('\t'.join(str(col) for col in row) + '\n' for row in engine.board)
                                    engine.king_rules()
                            else:
                                print("you clicked on the same square or you want to capture your own piece")
                                print("reseting the move")
                                engine.move = []
                    else:
                        print("Menu is not ready click on the chess board")
                #-- reserve right butotn
                if event.button == 3:
                    right_click = True


        screen.fill(pygame.Color("#696764"))
        #-- Drawing the chess board
        engine.draw_board()
        #-- setting the board to engine board
        board = engine.board
        #-- pass the new board to engine to draw the updated board
        engine.draw_pieces(board)
        #-- Python drawing the pieces
        engine.all_pieces.draw(screen)

        if len(engine.move) == 1:
            pygame.draw.rect(screen,pygame.Color("orange"),(col*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,TILE_SIZE),5)


        pygame.display.flip()
