import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1)
        self.moves_made.add(cell)

        #2)
        self.safes.add(cell)
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)

        #3)
        i , j = cell
        cells1 = [
            (i-1, j-1), (i-1, j), (i-1, j+1),
            (i, j-1),              (i, j+1),
            (i+1, j-1), (i+1, j), (i+1, j+1)
        ]
        cells2 = cells1.copy()
        #print(f"Cell will be worked: {cell}")
        #print(f"Neighbor Cells: {cells2}")

        #Remove cells that are outside of board
        for (i1, j1) in cells1:
            if (i1<=-1 or i1>=8) or (j1<=-1 or j1>=8):
                #print(f"first if, i1 = {i1}, j1 = {j1}")
                cells2.remove((i1, j1))

        cells1 = cells2.copy()

        #Remove cells that are in Safes list
        for (i1, j1) in cells1:       
            if (i1, j1) in self.safes and (i1, j1) in cells2:
                #print(f"Second if, i1 = {i1}, j1 = {j1}") 
                cells2.remove((i1, j1))

        cells1 = cells2.copy()

        #Remove cells that are in Mines list
        for (i1, j1) in cells1:
            if (i1, j1) in self.mines and (i1, j1) in cells2:
                #print(f"Third if, i1 = {i1}, j1 = {j1}")
                cells2.remove((i1, j1))
                count = count - 1
        
        cells1 = cells2.copy()    
        
        #print(f"Added info:{cells1}, count: {count}")
        self.knowledge.append(Sentence(cells1, count))

        #4)
        for stc1 in self.knowledge:
            stc1_cells = stc1.cells.copy()
            if len(stc1.cells) == stc1.count:
                for cell1 in stc1.cells:
                    self.mines.add(cell1)
                    stc1_cells.remove(cell1)
                    stc1.count = stc1.count - 1 
            elif stc1.count == 0 and len(stc1.cells) != 0:
                for cell2 in stc1.cells:
                    self.safes.add(cell2)
                    if cell2 in stc1_cells:
                        stc1_cells.remove(cell2)
            elif len(stc1.cells) == 0:
                self.knowledge.remove(stc1)
            stc1.cells = stc1_cells.copy()

        #5)
        for sentence1 in self.knowledge:
            set1 = sentence1.cells
            count1 = sentence1.count
            for sentence2 in self.knowledge:
                set2 = sentence2.cells
                count2 = sentence2.count
                if set1 ^ set2 == {None}:
                    break
                if (set1 in set2) or (set2 in set1):
                    STC = Sentence(set1 ^ set2, abs(count1 - count2))
                    self.knowledge.append(STC) 

        #print(f"Safes: {self.safes}")
        #print(f"Mades: {self.moves_made}")
        #print(f"Mines: {self.mines}")
        #print(f"Knowledge: {self.knowledge}")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for Move in self.safes:
            if Move not in self.moves_made and Move not in self.mines:
                self.moves_made.add(Move)
                return Move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        i = random.randrange(7)
        j = random.randrange(7)
        if (i,j) not in self.moves_made and (i, j) not in self.mines:
            self.moves_made.add((i,j))
            return (i,j)
        else:
            return None 

