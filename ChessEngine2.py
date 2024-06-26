"""
This is responsible for:
	- storing all the information about the current game state.
	- determining the valid moves
	- will keep a move log (for doing undo  and look back into current game)
"""

class GameState():
	def __init__(self):
		# board is a 8*8 2D list
		# each element is a 2 character long string consisting of
			# - lower case (b/w) as color
			# - upper case (R,N,B,Q,K or P) as piece name
		# in case the cell is empty then we store '--'
		self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
					['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
					['--', '--', '--', '--', '--', '--', '--', '--'],
					['--', '--', '--', '--', '--', '--', '--', '--'],
					['--', '--', '--', '--', '--', '--', '--', '--'],
					['--', '--', '--', '--', '--', '--', '--', '--'],
					['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			 		['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

		self.moveFunctions = {'P' : self.getPawnMoves, 'R' : self.getRookMoves, 'N' : self.getKnightMoves,
								'B' : self.getBishopMoves, 'Q' : self.getQueenMoves, 'K' : self.getKingMoves}
		self.whiteToMove = True
		self.moveLog = []
		#Keeping track of kings to make valid move calculation and castling easier.
		self.whiteKingLocation = (7,4)
		self.blackKingLocation = (0,4)

		#keep track of checkmate and stalemate
		self.checkMate = False
		self.staleMate = False

	'''
	A function to move pieces on the board and record them. (Won't work for castling, pawn-promotion and en-passant)
	'''
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = '--'  # empty the start cell
		self.board[move.endRow][move.endCol] = move.pieceMoved # keep the piece moved on the end cell
		self.moveLog.append(move) # record the move
		self.whiteToMove = not self.whiteToMove # swap the turn
		#UPDATE KING'S POSITION
		if move.pieceMoved == 'wK':
			self.whiteKingLocation = (move.endRow, move.endCol)
		if move.pieceMoved == 'bK':
			self.blackKingLocation = (move.endRow, move.endCol)
	'''
	Undo a move.
	'''
	def undoMove(self):
		if len(self.moveLog) == 0:
			print('No move done till now. Can\'t UNDO at the start of the game')
			return
		move = self.moveLog.pop()
		self.board[move.startRow][move.startCol] = move.pieceMoved
		self.board[move.endRow][move.endCol] = move.pieceCaptured
		self.whiteToMove = not self.whiteToMove
		#UPDATE KING'S POSITION
		if move.pieceMoved == 'wK':
			self.whiteKingLocation = (move.startRow, move.startCol)
		if move.pieceMoved == 'bK':
			self.blackKingLocation = (move.startRow, move.startCol)

	''' 
	Get a list of all the valis moves -> the moves that user can actually make. => Considering CHECKS.
	'''
	def getValidMoves(self):
		# 1) Get a List of all possible Moves
		moves = self.getAllPossibleMoves()
		# 2) Make a move from the list of possible moves
		for i in range(len(moves)-1, -1, -1): #travering in opposite direction cause we have to remove some elements from the middle.
			self.makeMove(moves[i])
			self.whiteToMove = not self.whiteToMove
		# 3) Generate all of the opponents move after making the move in previous stel
		# 4) Check if any of the opponents move leads to check -> if so remove the move from our list
			if self.inCheck():
				moves.remove(moves[i])
			self.whiteToMove = not self.whiteToMove
			self.undoMove()
		# 5) Return the final list of moves
		if len(moves) == 0:
			if self.inCheck():
				print("CHECK MATE! " + ('w' if not self.whiteToMove else 'b') + " wins")

				self.checkMate = True
			else:
				print("DRAW DUE TO STALEMATE")
				self.staleMate = True
		else:
			self.checkMate = False
			self.staleMate = False
		return moves

	'''
	Checks if the current player is under check
	'''
	def inCheck(self):
		if self.whiteToMove:
			return self.isUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
		else:
			return self.isUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

	'''
	Checks if sq (r,c) is under attack or not
	'''
	def isUnderAttack(self, r, c):
		self.whiteToMove = not self.whiteToMove # switch to opponent's turn
		opponentsMove = self.getAllPossibleMoves() #generate opponents move
		self.whiteToMove = not self.whiteToMove # switch back turns
		for move in opponentsMove:
			if move.endRow == r and move.endCol == c: #sq under attak
				return True
		return False

	'''
	Get a list of all possible moves -> Without considering CHECKS
	'''
	def getAllPossibleMoves(self):
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				piece = self.board[r][c][1]
				if not ((self.whiteToMove) ^ (turn == 'w')):
				# if (self.whiteToMove and turn == 'w') or (self.whiteToMove == False and turn == 'b'):
					if piece != '-':
						 self.moveFunctions[piece](r, c, moves) #call appropriate get piece move function
		return moves

	'''
	Get all possible moves for a pawn located at (r,c) and add the moves to the list.
	'''
	def getPawnMoves(self, r, c, moves):
		if self.whiteToMove and self.board[r][c][0] == 'w': # WHITE PAWN MOVES
			if self.board[r-1][c] == '--': # 1 square pawn advance
				moves.append(Move((r, c), (r-1, c), self.board))
				if r == 6 and self.board[r-2][c] == '--': # 2 square pawn advance
					moves.append(Move((r, c), (r-2, c), self.board))
			if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':  #  enemy pice to capture to the left
				moves.append(Move((r, c), (r-1, c-1), self.board))
			if c+1 < len(self.board) and self.board[r-1][c+1][0] == 'b': # enemy pice to capture to the right
				moves.append(Move((r, c), (r-1, c+1), self.board))


		if not self.whiteToMove and self.board[r][c][0] == 'b': # BLACK PAWN MOVES
			if self.board[r+1][c] == '--': # 1 square pawn advance
				moves.append(Move((r, c), (r+1, c), self.board))
				if r == 1 and self.board[r+2][c] == '--': # 2 square pawn advance
					moves.append(Move((r, c), (r+2, c), self.board))
			if c-1 >= 0 and self.board[r+1][c-1][0] == 'w': # enemy pice to capture to the left
				moves.append(Move((r, c), (r+1, c-1), self.board))
			if c+1 < len(self.board) and self.board[r+1][c+1][0] == 'w': # enemy pice to capture to the right
				moves.append(Move((r, c), (r+1, c+1), self.board))

	'''
	Get all possible moves for a Rook located at (r,c) and add the moves to the list.
	'''
	def getRookMoves(self, r, c, moves):
		# #UP THE FILE
		# for i in range(r-1,-1,-1):
		# 	#Empty Square
		# 	if self.board[i][c] == '--':
		# 		moves.append(Move((r, c), (i, c), self.board))
		# 	#Capture opponent's piece
		# 	elif self.board[i][c][0] != self.board[r][c][0]:
		# 		moves.append(Move((r, c), (i, c), self.board))
		# 		break
		# 	#Same Color piece
		# 	else:
		# 		break

		# #DOWN THE FILE
		# for i in range(r+1, len(self.board)):
		# 	#Empty Square
		# 	if self.board[i][c] == '--':
		# 		moves.append(Move((r, c), (i, c), self.board))
		# 	#Capture Oponent's piece
		# 	elif self.board[i][c][0] != self.board[r][c][0]:
		# 		moves.append(Move((r, c), (i, c), self.board))
		# 		break
		# 	# Same color piece
		# 	else:
		# 		break

		# #LEFT IN THE RANK
		# for i in range(c-1,-1,-1):
		# 	#Empty Square
		# 	if self.board[r][i] == '--':
		# 		moves.append(Move((r, c), (r, i), self.board))
		# 	#Capture Oponent's piece
		# 	elif self.board[r][i][0] != self.board[r][c][0]:
		# 		moves.append(Move((r, c), (r, i), self.board))
		# 		break
		# 	# Same color piece
		# 	else:
		# 		break

		# #RIGHT IN THE RANK
		# for i in range(c+1, len(self.board[r])):
		# 	#Empty Square
		# 	if self.board[r][i] == '--':
		# 		moves.append(Move((r, c), (r, i), self.board))
		# 	#Capture Oponent's piece
		# 	elif self.board[r][i][0] != self.board[r][c][0]:
		# 		moves.append(Move((r, c), (r, i), self.board))
		# 		break
		# 	# Same color piece
		# 	else:
		# 		break

		# -----------  ANOTHER WAY TO IMPLEMENT THIS   ---------- #

		directions = ((-1,0) , (1,0) , (0,-1), (0,1)) # up down left right
		enemyColor = 'b' if self.whiteToMove else 'w' # opponenet's color according to current turn
		for d in directions:
			for i in range(1,8):
				endRow = r + (d[0] * i)
				endCol = c + (d[1] * i)
				if endRow >=0 and endRow < len(self.board) and endCol >=0 and endCol < len(self.board[endRow]):
					if self.board[endRow][endCol] == '--': #Empty Square
						moves.append(Move((r, c), (endRow, endCol), self.board))
					elif self.board[endRow][endCol][0] == enemyColor: # capture opponent's piece
						moves.append(Move((r, c), (endRow, endCol), self.board))
						break
					else:
						break # same color piece
				else :
					break #off board

	'''
	Get all possible moves for a Knight located at (r,c) and add the moves to the list.
	'''
	def getKnightMoves(self, r, c, moves):
		directions = ((-1,-2) , (-2,-1), (1,-2), (2,-1), (1,2), (2,1), (-1,2), (-2,1))
		allyColor = 'w' if self.whiteToMove else 'b' # opponenet's color according to current turn
		for d in directions:
			endRow = r + d[0]
			endCol = c + d[1]
			if endRow >=0 and endRow < len(self.board) and endCol >=0 and endCol < len(self.board[endRow]):
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor:
					moves.append(Move((r, c), (endRow, endCol), self.board))

	'''
	Get all possible moves for a Bishop located at (r,c) and add the moves to the list.
	'''
	def getBishopMoves(self, r, c, moves):
		directions = ((-1,-1), (-1,1), (1,-1), (1,1)) # (top left) (top right) (bottom left) (bottom right)
		enemyColor = 'b' if self.whiteToMove else 'w' # opponenet's color according to current turn
		for d in directions:
			for i in range(1,8):
				endRow = r + (d[0] * i)
				endCol = c + (d[1] * i)
				if endRow >=0 and endRow < len(self.board) and endCol >=0 and endCol < len(self.board[endRow]):
					if self.board[endRow][endCol] == '--': #Empty Square
						moves.append(Move((r, c), (endRow, endCol), self.board))
					elif self.board[endRow][endCol][0] == enemyColor: # capture opponent's piece
						moves.append(Move((r, c), (endRow, endCol), self.board))
						break
					else:
						break # same color piece
				else :
					break #off board

	'''
	Get all possible moves for a Queen located at (r,c) and add the moves to the list.
	'''
	def getQueenMoves(self, r, c, moves):
		self.getRookMoves(r, c, moves)
		self.getBishopMoves(r, c, moves)

	'''
	Get all possible moves for a King located at (r,c) and add the moves to the list.
	'''
	def getKingMoves(self, r, c, moves):
		directions = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
		allyColor = 'w' if self.whiteToMove else 'b' # ally color according to current turn
		for d in directions:
			endRow = r + d[0]
			endCol = c + d[1]
			if endRow >=0 and endRow < len(self.board) and endCol >=0 and endCol < len(self.board[endRow]):
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor:
					moves.append(Move((r, c), (endRow, endCol), self.board))


class Move():

	#maps keys to values
	#For converting (row, col) to Chess Notations => (0,0) -> a8
	ranksToRows = {"1": 7 , "2": 6, "3": 5, "4": 4,
				   "5": 3, "6": 2, "7": 1, "8": 0 }
	rowsToRanks = {v:k  for k,v in ranksToRows.items()}
	filesToCols = {"a":0, "b":1, "c":2, "d":3,
				   "e":4, "f":5, "g":6, "h":7}
	colsToFiles = {v:k  for k,v in filesToCols.items()}

	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self. startRow][self. startCol] # can't be '--'
		self.pieceCaptured = board[self. endRow][self. endCol]  # can be '--' -> no piece was captured
		self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

	def getChessNotation(self):
		return self.getFileRank(self.startRow,self.startCol) + self.getFileRank(self.endRow,self.endCol)

	def getFileRank (self, r, c):
		return self.colsToFiles[c] + self.rowsToRanks[r]

	'''
	overriding equal to method
	'''
	def __eq__(self,other):
		return isinstance(other, Move) and self.moveId == other.moveId

