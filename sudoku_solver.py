import string

BLANK_PUZZLE = ['\n\n\n' for i in range(0,81)]

"""
sudoku_solver.SudokuSolver
    This class is the simplest object to help solve sudoku puzzles.

sudoku_solver.ContradictionSolver
    This class uses contradictions to eliminate possibilities and solve sudoku puzzles.
"""

class SudokuSolver:
    """
    SudokuSolver object.

    Provides solving, reading, and basic notes for solving a sudoku puzzle.

    Basic Usage::
    >>> import sudoku_solver
    >>> p = sudoku_solver.SudokuSolver('123...456...')
    >>> p.get_reduced_puzzle()
    '123...456........................................................................'
    """

    def __init__(self, sudoku_string_):
        """
        Creates SudokuSolver class.

        param sudoku_string_: puzzle encoding for new puzzle.

        returns SudokuSolver object.
        """
        puzzle_array = []
        processor = 0
        while processor < len(sudoku_string_) and len(puzzle_array) < 81:
            if sudoku_string_[processor].isnumeric():
                puzzle_array.append(sudoku_string_[processor])
            elif sudoku_string_[processor] == '\n' or sudoku_string_[processor] == '\r':
                # This was tricky. HTML form newlines aren't \n, they are \r
                pass
            else:
                puzzle_array.append(' ')
            processor = processor + 1
        while len(puzzle_array) < 81:
            puzzle_array.append(' ')
        self.puzzle_array = puzzle_array
        self.puzzle_string = sudoku_string_
        self.check_valid_puzzle()
        self.build_possibilities()
        # if self.check_valid_solution() is False:
        #    pass #TODO: come up with error handling...see if we can make this not so slow

    def check_valid_puzzle(self) -> None:
        """
        Checks that the puzzle created is valid. Raises ValueError if invalid.
        """
        for i in range(0, 9):
            if not self.check_valid_box(i):
                raise ValueError("Invalid puzzle. Bad box.")
            if not self.check_valid_row(i):
                raise ValueError("Invalid puzzle. Bad row.")
            if not self.check_valid_column(i):
                raise ValueError("Invalid puzzle. Bad column.")

    def check_valid_solution(self) -> bool:
        """
        Checks that a solution generated by the class is valid.

        Returns: bool. True if the solution is valid. False if invalid.
        """
        try:
            # Uses the reduced puzzle to create a new puzzle. Returns false if an error is raised.
            temp_puzzle = SudokuSolver(self.get_reduced_puzzle())
            return True
        except:
            return False

    def check_valid_box(self, box_number) -> bool:
        """
        Check that a box of cells is valid under sudoku rules.

        param box_number: int. The number of the box to be checked.

        Returns: bool. True if valid. False in invalid.
        """
        # Get the index of the first cell.
        box_start = self.get_box_start_index(box_number)
        # Create an empty list. We'll insert each cell's contents.
        box = []
        box.append(self.puzzle_array[box_start])
        box.append(self.puzzle_array[box_start + 1])
        box.append(self.puzzle_array[box_start + 2])
        box.append(self.puzzle_array[box_start + 9])
        box.append(self.puzzle_array[box_start + 10])
        box.append(self.puzzle_array[box_start + 11])
        box.append(self.puzzle_array[box_start + 18])
        box.append(self.puzzle_array[box_start + 19])
        box.append(self.puzzle_array[box_start + 20])

        # Check to see if any numbers are duplicated. If it is, return False.
        for i in range(1, 10):
            if box.count(str(i)) > 1:
                return False

        return True

    def check_valid_row(self, row_number) -> bool:
        """
        Check to see if a row is valid under sudoku rules.

        param row_number: number of row to check.

        Returns: bool. True if valid, False if invalid.
        """
        # Get a list with all the numbers in the row.
        row = self.puzzle_array[row_number * 9 : row_number * 9 + 9 :]
        # If a number is duplicated return false.
        for i in range(1, 10):
            if row.count(str(i)) > 1:
                return False
        return True

    def check_valid_column(self, column_number) -> bool:
        """
        Check if a column in the puzzle is valid.

        param column_number: int. Number of column to check.

        Returns: bool. True if valid. False if invalid.
        """
        # Make a list containing the selected column.
        column = self.puzzle_array[column_number::9]
        # If a number is duplicated return false.
        for i in range(1, 10):
            if column.count(str(i)) > 1:
                return False
        return True

    def get_cell_box_number(self, cell_number):
        raise NotImplementedError('TODO: get_cell_box_number')

    def get_cell_row_number(self, cell_number):
        raise NotImplementedError('TODO: get_cell_row_number')

    def get_cell_column_number(self, column_number):
        raise NotImplementedError('TODO: get_cell_column_number')

    def __str__(self) -> str:
        """
        Gets a printable version of the puzzle.

        Returns: str. printable string in puzzle format.
        """
        sudoku_string = ' --- --- ---\n'

        for i in range(len(self.puzzle_array)):
            if i % 27 == 0 and i != 0:
                sudoku_string = sudoku_string + '|\n --- --- ---\n'
            elif i % 9 == 0 and i != 0:
                sudoku_string = sudoku_string + '|\n'
            if i % 3 == 0:
                sudoku_string = sudoku_string + '|'

            sudoku_string = sudoku_string + self.puzzle_array[i]

        sudoku_string = sudoku_string + '|\n --- --- ---'

        return sudoku_string

    def print_possibilities(self) -> None:
        """
        Prints solved cells and nothing else.

        TODO: figure out what to do with this function.
        """
        for i in range(81):
            if i % 9 == 0 and i != 0:
                print()
            if len(self.possibilities[i]) == 1:
                print(self.possibilities[i][0], end='')
            else:
                print(' ', end='')
        print()

    def build_possibilities(self) -> None:
        """
        Builds the possible solutions for all of the cells. If a cell is solved it continues running
        until no more are solved during an iteration.

        Uses row, column, and box elimination, and can identify unique solutions for a number in a 
        box.

        Saves the possibilities as a class attribute.
        """
        self.possibilities = [[str(i) for i in range(1, 10)] for i in range(0, 81)]
        for i in range(0, 81):
            if self.puzzle_array[i] != ' ':
                self.possibilities[i] = [self.puzzle_array[i]]

        old_possibilities = self.number_of_possibilites()
        new_possibilities = 0
        while old_possibilities > new_possibilities:
            old_possibilities = self.number_of_possibilites()

            for i in range(0, 9):
                self.reduce_row(i)

            for i in range(0, 9):
                self.reduce_column(i)

            for i in range(0, 9):
                self.reduce_box(i)

            for i in range(0, 9):
                self.find_unique_possibilities_by_box(i)

            new_possibilities = self.number_of_possibilites()

    def reduce_row(self, row_number) -> None:
        """
        Reduces possibilities in a row.

        param row_number: the number of the row to reduce.
        """
        i = row_number * 9

        numbers_to_eliminate = []

        while i < (row_number * 9) + 9:
            if len(self.possibilities[i]) == 1:
                numbers_to_eliminate.append(self.possibilities[i][0])
            i = i + 1

        for number in numbers_to_eliminate:
            i = row_number * 9
            while i < (row_number * 9) + 9:
                if len(self.possibilities[i]) != 1 and number in self.possibilities[i]:
                    self.possibilities[i].pop(self.possibilities[i].index(number))
                i = i + 1

    def reduce_column(self, column_number) -> None:
        i = column_number

        numbers_to_eliminate = []

        while i < 81:
            if len(self.possibilities[i]) == 1:
                numbers_to_eliminate.append(self.possibilities[i][0])
            i = i + 9

        for number in numbers_to_eliminate:
            i = column_number
            while i < 81:
                if len(self.possibilities[i]) != 1 and number in self.possibilities[i]:
                    self.possibilities[i].pop(self.possibilities[i].index(number))
                i = i + 9

    def get_box_start_index(self, box_number) -> int:
        """
        Get the index of the first cell in a box based on box number.

        param box_number: the number of box to the index for.

        Returns: int. The index of the upper left cell in the box.
        """
        if box_number == 0:
            return 0
        elif box_number == 1:
            return 3
        elif box_number == 2:
            return 6
        elif box_number == 3:
            return 27
        elif box_number == 4:
            return 30
        elif box_number == 5:
            return 33
        elif box_number == 6:
            return 54
        elif box_number == 7:
            return 57
        elif box_number == 8:
            return 60

    def reduce_box(self, box_number) -> None:
        """
        Reduces the possibilities in a box based on given or solved cells in the box.

        param int box_number: the box number to be reduced.

        Returns: None.
        """
        i = self.get_box_start_index(box_number)
        numbers_to_eliminate = []

        for j in range(0, 3):
            if len(self.possibilities[i]) == 1:
                numbers_to_eliminate.append(self.possibilities[i][0])
            i = i + 1
            if len(self.possibilities[i]) == 1:
                numbers_to_eliminate.append(self.possibilities[i][0])
            i = i + 1
            if len(self.possibilities[i]) == 1:
                numbers_to_eliminate.append(self.possibilities[i][0])
            i = i + 7

        for number in numbers_to_eliminate:
            i = self.get_box_start_index(box_number)
            for j in range(0, 3):
                if len(self.possibilities[i]) != 1 and number in self.possibilities[i]:
                    self.possibilities[i].pop(self.possibilities[i].index(number))
                i = i + 1
                if len(self.possibilities[i]) != 1 and number in self.possibilities[i]:
                    self.possibilities[i].pop(self.possibilities[i].index(number))
                i = i + 1
                if len(self.possibilities[i]) != 1 and number in self.possibilities[i]:
                    self.possibilities[i].pop(self.possibilities[i].index(number))
                i = i + 7

    def find_unique_possibilities_by_box(self, box_number) -> None:
        # TODO: test this more, this one of all of them is the scariest so far
        box_start = self.get_box_start_index(box_number)
        all_possibilities = []
        numbers_to_reduce = []
        not_to_eliminate = []
        i = box_start

        for j in range(0, 3):
            if len(self.possibilities[i]) > 1:
                all_possibilities = all_possibilities + self.possibilities[i]
            else:
                not_to_eliminate.append(self.possibilities[i][0])
            i = i + 1

            if len(self.possibilities[i]) > 1:
                all_possibilities = all_possibilities + self.possibilities[i]
            else:
                not_to_eliminate.append(self.possibilities[i][0])
            i = i + 1

            if len(self.possibilities[i]) > 1:
                all_possibilities = all_possibilities + self.possibilities[i]
            else:
                not_to_eliminate.append(self.possibilities[i][0])
            i = i + 7

        for j in range(0, 10):
            if all_possibilities.count(str(j)) == 1 and str(j) not in not_to_eliminate:
                numbers_to_reduce.append(str(j))

        for number in numbers_to_reduce:
            i = box_start
            for j in range(0, 3):
                if len(self.possibilities[i]) > 1 and (number in self.possibilities[i]):
                    self.possibilities[i] = [number]
                i = i + 1
                if len(self.possibilities[i]) > 1 and (number in self.possibilities[i]):
                    self.possibilities[i] = [number]
                i = i + 1
                if len(self.possibilities[i]) > 1 and (number in self.possibilities[i]):
                    self.possibilities[i] = [number]
                i = i + 7

    def number_of_possibilites(self) -> int:
        """
        Count the number of possibilities remaining in the puzzle.

        Returns: int.
        """
        possibilities = 0

        for i in range(0, 81):
            possibilities = possibilities + len(self.possibilities[i])
        return possibilities

    def get_possibilities(self) -> list:
        """
        Get the remaining possibilities in a puzzle.

        Returns: list (of lists). 
        """
        return self.possibilities

    def get_reduced_puzzle(self) -> string:  # TODO: expand testing for this
        """
        Get the string encoding of the puzzle, with any solved cells, as a string.

        Returns: string.
        """
        reduced_puzzle = ''
        for possibility in self.possibilities:
            if len(possibility) == 1:
                reduced_puzzle = reduced_puzzle + possibility[0]
            else:
                reduced_puzzle = reduced_puzzle + '.'
        return reduced_puzzle
    
    def get_possibilities_for_web(self) -> list:
        """
        Get the string encodings of the reduced puzzle. Returns a list of strings.
        For cells that have multiple possibilities still, it will format them so that
        the preformatting checker will leave them alone and they'll be readable.

        Returns: list (of strings).
        """
        def build_hints_string(remaining_hints) -> str:
            hint_string = ''
            index = 1
            for letter in remaining_hints:
                while int(letter) != index:
                    hint_string = hint_string + ' '
                    if index % 3 == 0:
                        hint_string = hint_string + '\n'
                    index += 1
                hint_string = hint_string + letter
                if index % 3 ==0:
                    hint_string = hint_string + '\n'
                index = index+1
                
            return hint_string
        
        formatted_list = []

        for cell in self.possibilities:
            if len(cell) == 1:
                formatted_list.append(cell)
            else:
                formatted_list.append( build_hints_string(cell) )

        return formatted_list
    
class ContradictionSolver:
    """
    ContradicionSolver object

    Uses contradictions to find solutions to sudoku puzzles.
    """
    def __init__(self) -> None:
        pass
    # TODO: use keyword arguments to build from either puzzle string, or SudokuSolver object
    