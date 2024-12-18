import itertools
import random


class Minesweeper:
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


class Sentence:
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
        return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI:
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

        This function:
            1) Marks the cell as a move that has been made.
            2) Marks the cell as safe.
            3) Adds a new sentence to the AI's knowledge base.
            4) Marks any additional cells as safe or as mines if it can be concluded.
            5) Infers new sentences from existing knowledge.
        """
        # Step 1: Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Step 2: Mark the cell as safe
        self.mark_safe(cell)

        # Step 3: Add a new sentence to the knowledge base
        neighbors = self.find_cell_neighbors(cell)
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        # Step 4: Mark cells as safe or mines based on current knowledge
        self.update_knowledge_base()

        # Step 5: Infer new sentences from existing knowledge
        self.infer_new_sentences()

    def update_knowledge_base(self):
        """
        Updates the knowledge base by marking cells as safe or mines
        whenever possible, based on existing knowledge.
        """
        changes = True
        while changes:
            changes = False
            # Check each sentence for known safes and mines
            for sentence in self.knowledge:
                safes = sentence.known_safes().copy()
                mines = sentence.known_mines().copy()

                # Mark cells as safe
                if safes:
                    changes = True
                    for safe in safes:
                        self.mark_safe(safe)

                # Mark cells as mines
                if mines:
                    changes = True
                    for mine in mines:
                        self.mark_mine(mine)

        # Remove empty sentences
        self.knowledge = [s for s in self.knowledge if s.cells]

    def infer_new_sentences(self):
        """
        Infers new sentences based on subset relationships in the knowledge base.
        """
        inferred = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 != s2 and s1.cells.issubset(s2.cells):
                    # Infer a new sentence
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    new_sentence = Sentence(new_cells, new_count)

                    # Ensure the new sentence is not redundant
                    if (
                        new_sentence not in self.knowledge
                        and new_sentence not in inferred
                    ):
                        inferred.append(new_sentence)

        # Add all inferred sentences to the knowledge base
        self.knowledge.extend(inferred)

    def find_cell_neighbors(self, cell):
        row, col = cell
        candidates = (
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1),
        )
        neighbors = []
        for candidate in candidates:
            r, c = candidate
            if (
                candidate not in self.moves_made
                and 0 <= r < self.height
                and 0 <= c < self.width
            ):
                neighbors.append(candidate)
        return neighbors

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        possible_moves = []
        for c in self.safes:
            if c not in self.moves_made:
                possible_moves.append(c)
        return random.choice(possible_moves) if possible_moves else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = [
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
            if (row, col) not in self.moves_made and (row, col) not in self.mines
        ]

        # If there are no valid moves, return None
        if not possible_moves:
            return None

        # Randomly select a move from the possible moves
        return random.choice(possible_moves)
