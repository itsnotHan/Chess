"""
This class is responsible for storing all the information about the current state of a chess game. It will also be
responsible for determining the valid moves at the current state. It will also keep a move log.
"""


class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bP", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, "K": self.getkingMoves}
        self.whiteToMove = True
        self.moveLog = []

#will not work for castling, en passant, and pawn promotion

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove #switch turns

    def undoMove(self):
        if len(self.moveLog) !=0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch turns

    #all moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    #All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols  in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c, moves) #calls appropriate move functions based on piece type
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list 
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c), (r-2, c), self.board))
            if c-1 >= 0: #captures to the left, so we can't capture piece across the board
                if self.board[r-1][c-1][0] == "b": #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else:
            if self.board[r+1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": #2 square pawn advance
                    moves.append(Move((r,c), (r+2, c), self.board))
            if c-1 >= 0: #captures to the left, so we can't capture piece across the board
                if self.board[r+1][c+1][0] == "w": #enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
            if c+1 <= 7: #captures to the right
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))



    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list 
    '''

    def getRookMoves(self, r, c, moves):
        pass

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list 
    '''

    def getKnightMoves(self, r, c, moves):
        pass

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list 
    '''

    def getBishopMoves(self, r, c, moves):
        pass

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list 
    '''

    def getQueenMoves(self, r, c, moves):
        pass

    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list 
    '''

    def getkingMoves(self, r, c, moves):
        pass



class Move():
    #map values to keys
    #key: value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0 }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    def __init__(self, startsQ, endQ, board):
        self.startRow = startsQ[0]
        self.startCol = startsQ[1]
        self.endRow = endQ[0]
        self.endCol = endQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False



    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]